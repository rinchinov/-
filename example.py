from problem import Problem


def solve_5_1():
    """ Пример использовния для задачи 5.1, стр 83
    Л.Г ЛАБСКЕР, Л.О. БАБЕШКО "Теория массового обслуживания в экономической сфере"  """
    task = Problem(1, 3, 2, 2.5, 3, "Задача 5.1")
    print("1)")
    task.param4(pretty_output=True)
    print("2)")
    task.param6(pretty_output=True)
    task.param7(pretty_output=True)
    print("3)")
    task.param9(pretty_output=True)
    print("4)")
    task.param10()
    task.param11()
    task.param12(pretty_output=True)
    print("5)")
    task.param13(pretty_output=True)
    task.imitation_modelling(60, 2000, 200)
    return task.solve_diff(60, 10000)

result = solve_5_1()
