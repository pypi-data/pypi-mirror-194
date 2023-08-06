from solver_copy import solver
from dio import dio
from cobra.flux_analysis import flux_variability_analysis
import re


io = dio()

#Ec1 reconstruction
# Ec1 = io.read_sbml_dModel('../iAF1260.xml')
#
# DAPDC = Ec1.reactions.get_by_id('DAPDC')
# DAPDC.upper_bound = 0
# DAPDC.lower_bound = 0
#
# HSST = Ec1.reactions.get_by_id('HSST')
# HSST.upper_bound = 0
# HSST.lower_bound = 0
#
# PHEt2rpp = Ec1.reactions.get_by_id('PHEt2rpp')
# PHEt2rpp.upper_bound = 0
# PHEt2rpp.lower_bound = 0
#
# sub = ['EX_arg__L_e', 'EX_lys__L_e', 'EX_met__L_e', 'EX_phe__L_e']
# sub_dir = ['maximum', 'maximum', 'maximum', 'maximum']
# Ec1.change_objective('BIOMASS_Ec_iAF1260_core_59p81M', 'maximum', sub, sub_dir, fraction_of_optimum=0.95)
#
# Ec1.modify_reaction('EX_lys__L_e', 'lower', 'lys/(1+lys)')
# Ec1.modify_reaction('EX_met__L_e', 'lower', 'met/(1+met)')
#
# models_dict = {'iAF1260': Ec1}
# states = {'x_iAF1260': 0.5, 'arg': 1.5, 'lys': 0, 'met': 1.6, 'phe': 1}
# derivatives_description = {'arg':'iAF1260_EX_arg__L_e', 'lys': 'iAF1260_EX_lys__L_e', 'met':'iAF1260_EX_met__L_e', 'phe': 'iAF1260_EX_phe__L_e'}

Ec2 = io.read_sbml_dModel('../iAF1260.xml')

sub = ['EX_glc__D_e']
sub_dir = ['maximum']
Ec2.change_objective('BIOMASS_Ec_iAF1260_core_59p81M', 'maximum', sub, sub_dir, fraction_of_optimum=0.95)
Ec2.modify_reaction('EX_glc__D_e', 'lower', '-2000*glc/(1+glc)')

solver2 = solver()
models_dict = {'iAF1260': Ec2}
states = {'x_iAF1260': 0.5, 'glc': 10}
derivatives_description = {'glc':'iAF1260_EX_glc__D_e'}
# result = solver2.simulate(models_dict, states, derivatives_description, 1)

states_names = list(states.keys())
states_value = list(states.values())
states_var = globals()
for i in range(0, len(states_value)):
    states_var['%s' % states_names[i]] = states_value[i]

##  接下来应该是写一个for循环，一个一个模型地结合酶动力学计算FVA优化结果，得到需要的flux值
model_names = list(models_dict.keys())
for model_name in model_names:
    #  读取每个模型中修改后的酶动力学反应
    model_temp = models_dict[model_name]
    dreactions = model_temp.dReactions

    #  根据酶动力学模型计算flux值
    for dreaction in dreactions:
        print(glc)
        print(glc/(glc+1))
        print(dreaction.equation)
        print(exec(dreaction.equation))
        print(model_temp.volume / model_temp.weight)
        exec('flux_value = (' + dreaction.equation + ') * (model_temp.volume / model_temp.weight)')  ## ？？测试一下state里没有eqution对应物质的情况
        print(flux_value)
        ##  修改对应反应的反应上下限
        if dreaction.bound_direction.startswith("upper"):
            dreaction.reaction.upper_bound = flux_value
        elif (dreaction.bound_direction.startswith("lower")):
            dreaction.reaction.lower_bound = flux_value
        elif (dreaction.bound_direction.startswith("both")):
            dreaction.reaction.upper_bound = 1000
            dreaction.reaction.lower_bound = -1000  ## 避免上下限调整时出bug
            dreaction.reaction.upper_bound = flux_value
            dreaction.reaction.lower_bound = flux_value

    #  使用FVA计算得到优化后的flux值  ？？测试一下不可解的情况，该怎么处理？
    sub_objectives = model_temp.sub_objectives
    sub_objective_directions = model_temp.sub_objective_directions
    flux_values = flux_variability_analysis(model_temp, reaction_list=sub_objectives,
                                            fraction_of_optimum=model_temp.fraction_of_optimum)

    #  得到次级目的反应的flux值，变量名为model名+_+reaction_id
    rxnsFluxValue = globals()
    for i in range(0, len(sub_objectives)):
        rxnsFluxValue[model_name + '_' + sub_objectives[i].id] = flux_values.at[
            sub_objectives[i].id, sub_objective_directions[i]]
        ##  加入一个环节  由于设定了几个次级目的反应的flux值，必将影响主要优化目标的flux值，所以把计算得到的次级目的反应flux值给赋值回去再计算objective
        ##  好像没啥用，反正都是在这个线性空间里面去求解objective的最大最小值，除非把上下限设置得紧密一些
        # sub_objectives[i].upper_bound = 1000
        # sub_objectives[i].lower_bound = -1000  ## 避免上下限调整时出bug
        # sub_objectives[i].upper_bound = flux_values.at[sub_objectives[i].id, "maximum"]
        # sub_objectives[i].lower_bound = flux_values.at[sub_objectives[i].id, "minimum"]

    #  使用FBA计算得到objective优化后的flux值  变量名为model名+_+mu
    solution = model_temp.optimize()
    if solution.status == "infeasible":
        rxnsFluxValue[model_name + '_mu'] = 0
    else:
        rxnsFluxValue[model_name + '_mu'] = solution.objective_value

##  最后是根据输入的时间导数公式和优化后得到的flux，计算时间导数并得到外界物质浓度变化情况
derivatives = []
rxnsFluxValue_keys = list(rxnsFluxValue.keys())
derivatives_keys = list(derivatives_description.keys())
for state_name in states_names:
    derivative = 0
    if state_name.startswith("x_"):  # 计算菌落生长率对应时间导数
        model_name = state_name.split("_", 1)[1]  # 得到state中的model名
        model_mu = model_name + '_mu'  # 优化后的生长率flux值变量名
        if model_mu in rxnsFluxValue_keys:  # 计算了这个菌的生长率, derivatives就不为0
            derivative = states[state_name] * rxnsFluxValue[model_mu]
    else:  # 计算物质对应时间导数
        # if state_name in derivatives_keys:  # 要求计算这种物质时间导数
        #     derivative_description = derivatives_description[state_name]  # 得到该物质的计算公式
        #     exec('derivative = '+ derivative_description)
        if state_name in derivatives_keys:  # 要求计算这种物质时间导数
            derivative_description = derivatives_description[state_name]  # 得到该物质的计算公式
            items = re.split('[+-]', derivative_description)
            for item in items:
                model_weight = 'x_' + item.split("_", 1)[0]
                exec('rxnsFluxValue[item] =' + model_weight + '*' + item)
            exec('derivative = ' + derivative_description)
    derivatives.append(derivative)

#  第二次循环
#  按调用函数传入的state键作为变量名，储存这个函数传入的浓度数据
states_names = list(states.keys())
states_value = [(states_value[i] + derivatives[i]) for i in range(0, len(states_value))]
for i in range(0, len(states_value)):
    states_var['%s' % states_names[i]] = states_value[i]

model_names = list(models_dict.keys())
for model_name in model_names:
    #  读取每个模型中修改后的酶动力学反应
    model_temp = models_dict[model_name]
    dreactions = model_temp.dReactions

    #  根据酶动力学模型计算flux值
    for dreaction in dreactions:
        print(glc)
        print(glc/(glc+1))
        print(dreaction.equation)
        print(exec(dreaction.equation))
        print(model_temp.volume / model_temp.weight)
        exec('flux_value = (' + dreaction.equation + ') * (model_temp.volume / model_temp.weight)')  ## ？？测试一下state里没有eqution对应物质的情况
        print(flux_value)
        ##  修改对应反应的反应上下限
        if dreaction.bound_direction.startswith("upper"):
            dreaction.reaction.upper_bound = flux_value
        elif (dreaction.bound_direction.startswith("lower")):
            dreaction.reaction.lower_bound = flux_value
        elif (dreaction.bound_direction.startswith("both")):
            dreaction.reaction.upper_bound = 1000
            dreaction.reaction.lower_bound = -1000  ## 避免上下限调整时出bug
            dreaction.reaction.upper_bound = flux_value
            dreaction.reaction.lower_bound = flux_value

    #  使用FVA计算得到优化后的flux值  ？？测试一下不可解的情况，该怎么处理？
    sub_objectives = model_temp.sub_objectives
    sub_objective_directions = model_temp.sub_objective_directions
    flux_values = flux_variability_analysis(model_temp, reaction_list=sub_objectives,
                                            fraction_of_optimum=model_temp.fraction_of_optimum)

    #  得到次级目的反应的flux值，变量名为model名+_+reaction_id
    rxnsFluxValue = globals()
    for i in range(0, len(sub_objectives)):
        rxnsFluxValue[model_name + '_' + sub_objectives[i].id] = flux_values.at[
            sub_objectives[i].id, sub_objective_directions[i]]
        ##  加入一个环节  由于设定了几个次级目的反应的flux值，必将影响主要优化目标的flux值，所以把计算得到的次级目的反应flux值给赋值回去再计算objective
        ##  好像没啥用，反正都是在这个线性空间里面去求解objective的最大最小值，除非把上下限设置得紧密一些
        # sub_objectives[i].upper_bound = 1000
        # sub_objectives[i].lower_bound = -1000  ## 避免上下限调整时出bug
        # sub_objectives[i].upper_bound = flux_values.at[sub_objectives[i].id, "maximum"]
        # sub_objectives[i].lower_bound = flux_values.at[sub_objectives[i].id, "minimum"]

    #  使用FBA计算得到objective优化后的flux值  变量名为model名+_+mu
    solution = model_temp.optimize()
    if solution.status == "infeasible":
        rxnsFluxValue[model_name + '_mu'] = 0
    else:
        rxnsFluxValue[model_name + '_mu'] = solution.objective_value

##  最后是根据输入的时间导数公式和优化后得到的flux，计算时间导数并得到外界物质浓度变化情况
derivatives = []
rxnsFluxValue_keys = list(rxnsFluxValue.keys())
derivatives_keys = list(derivatives_description.keys())
for state_name in states_names:
    derivative = 0
    if state_name.startswith("x_"):  # 计算菌落生长率对应时间导数
        model_name = state_name.split("_", 1)[1]  # 得到state中的model名
        model_mu = model_name + '_mu'  # 优化后的生长率flux值变量名
        if model_mu in rxnsFluxValue_keys:  # 计算了这个菌的生长率, derivatives就不为0
            derivative = states[state_name] * rxnsFluxValue[model_mu]
    else:  # 计算物质对应时间导数
        # if state_name in derivatives_keys:  # 要求计算这种物质时间导数
        #     derivative_description = derivatives_description[state_name]  # 得到该物质的计算公式
        #     exec('derivative = '+ derivative_description)
        if state_name in derivatives_keys:  # 要求计算这种物质时间导数
            derivative_description = derivatives_description[state_name]  # 得到该物质的计算公式
            items = re.split('[+-]', derivative_description)
            for item in items:
                model_weight = 'x_' + item.split("_", 1)[0]
                exec('rxnsFluxValue[item] =' + model_weight + '*' + item)
            exec('derivative = ' + derivative_description)
    derivatives.append(derivative)

#
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.integrate import odeint
# class test1():
#
#     def __init__(self):
#         self.num = 2
#         self.states_var = globals()
#
#     def diff(self, y, x):
#         return np.array(self.num/x)
#
#     def cal(self):
#         self.states_var['x0'] = 5
#         x = np.linspace(x0, 10, 100)  # 给出x范围，(起始，终值，分割段数)
#         y = odeint(self.diff, 0, x)  # 设函数初值为0，即f(1)=0
#         plt.xlabel('x')
#         plt.ylabel('y')
#         plt.title("y=ln(x)")
#         plt.grid()#绘制网格
#         plt.plot(x, y)  # 将x,y两个数组进行绘图
#         plt.show()#打印图表
#
#
# if __name__ == '__main__':
#     pro = test1()
#     pro.cal()
#
#
# # import numpy as np
# # import matplotlib.pyplot as plt
# # from scipy.integrate import odeint
#
# # def diff(y, x):
# # 	return np.array(1/x)
# # 	# 上面定义的函数在odeint里面体现的就是dy/dx =1/x
# # x = np.linspace(1, 10, 100)  # 给出x范围，(起始，终值，分割段数)
# # y = odeint(diff, 0, x)  # 设函数初值为0，即f(1)=0
# # plt.xlabel('x')
# # plt.ylabel('y')
# # plt.title("y=ln(x)")
# # plt.grid()#绘制网格
# # plt.plot(x, y)  # 将x,y两个数组进行绘图
# # plt.show()#打印图表
#
