# -*- coding: utf-8 -*-
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as pp


def pretty_output(method):
    def wrapped(pretty_output=False):
        res = method()
        if pretty_output:
            print("{}: {}".format(method.__doc__, res))
        return res
    return wrapped


class Problem():
    def __init__(self, n, m, request_time, service_time, queue_max, name="Задача 5.1"):
        """ Одноканальная СМО с ожиданием и ограничением на длину очереди
        Этот класс реализует методы описанные в таблице 5.2(на стр 80-82)
         Л.Г ЛАБСКЕР, Л.О. БАБЕШКО "Теория массового обслуживания в экономической сфере" """
        self.name = name
        self.n = n
        self.m = m
        self._lambda = 1 / request_time
        self._mu = 1 / service_time
        self._m = queue_max
        self._p_via_ro = list()
        self._p_via_T = list()
        self._ro = self._lambda / self._mu
        self._T_service = service_time
        self._T = request_time
        self._add_pretty_output()
        self.imitation = None
        self.A0 = np.zeros(self.n + self.m + 1)
        self.A0[0] = 1

    def _add_pretty_output(self):
        for attr in dir(self):
            if callable(getattr(self, attr)) and "param" in attr:
                setattr(self, attr, pretty_output(getattr(self, attr)))

    def param1(self):
        """ Показатель нагрузки (трафик) системы """
        return self._ro

    def param2(self):
        """ Вероятности состояний СМО, выраженные через показатель нагрузки р """
        if self._ro != 1:
            self._p_via_ro.append((1 - self._ro) / (1 - pow(self._ro, self._m + 2)))
        else:
            self._p_via_ro.append(1 / (self._m + 2))
        for t in range(self._m):
            self._p_via_ro.append(self._p_via_ro[-1] * self._ro)
        return self._p_via_ro

    def param3(self):
        """ Вероятности состояний СМО, выраженные через средний интервал времени T между поступающими заявками и среднее
         время Т_об обслуживания одной заявки"""
        T_div = self._T_service / self._T
        if self._T != self._T_service:
            self._p_via_T.append((self._T - self._T_service) * pow(self._T, self._m + 1) /
                                 (pow(self._T, self._m + 2) - pow(self._T_service, self._m + 2)))
        else:
            self._p_via_T.append(1 / (self._m + 2))
        for t in range(self._m):
            self._p_via_T.append(self._p_via_T[-1] * T_div)
        return self._p_via_T

    def param4(self):
        """ Вероятность отказа """
        if self._ro != 1:
            self._p_denial = (pow(self._ro, self._m + 1) * (1 - self._ro)) / (1 - pow(self._ro, self._m + 2))
        else:
            self._p_denial = 1 / (self._m + 2)
        return self._p_denial

    def param5(self):
        """  Вероятность тoro, что заявка будет принята в систему (не получит отказ)"""
        return 1 - self.param4()

    def param6(self):
        """ Oтносительная пропускная способность СМО """
        self._Q = 1 - self.param4()
        return 1 - self.param4()

    def param7(self):
        """ Абсолютная пропускная способность СМО """
        return self._lambda * self._Q

    def param8(self):
        """ Интeнсивность выходящегo потока заявок """
        return self.param7()

    def param9(self):
        """ Среднее число заявок в очереди """
        p = self._ro
        m = self._m
        if self._ro != 1:
            self._N_queue = (p*p*(1-pow(p,m)*(m+1-m*p)))/((1-pow(p,m+2))*(1-p))
        else:
            self._N_queue = (m*(m+1)) / (2*(m+2))
        return self._N_queue

    def param10(self):
        """ Среднее число заявок, находящихся под обслуживанием """
        self._N_service = self._ro * self._Q
        return self._N_service

    def param11(self):
        """ Среднее число заявок, находящихся в системе( как в очереди, так и под обслуживанием). """
        self._N_system = self._N_queue + self._N_service
        return self._N_system

    def param12(self):
        """ Среднее время ожидания заявки в очереди """
        self._T_queue = self._N_queue / self._lambda
        return self._T_queue

    def param13(self):
        """ Среднее время пребывания заявки в системе (как в очереди, так и под обслуживанием) """
        self._T_system = self._N_system / self._lambda
        return self._T_system

    def param14(self):
        """ Среднее время обслуживания одной относящееся только к обслуженным заявкам"""
        return self._T_service

    def param15(self):
        """ Среднее время обслуживания одной относещееся ко всем заявкам, как обслуженным, так и получившим отказ"""
        self._T_service_all = self._N_service / self._lambda
        return self._T_service_all

    @staticmethod
    def _deriv(A, t, Ab):
        return np.dot(Ab, A)

    @staticmethod
    def _prepare_matrix(size_, mu_, lambda_ ):
        result = np.zeros((size_, size_))
        for i in range(0, size_ - 1):
            result[i][i+1] = mu_
            result[i+1][i] = lambda_
            result[i][i] = - lambda_- mu_
        result[0][0] = -lambda_
        result[size_ - 1][size_ - 1] = -mu_
        return result

    def solve_diff(self, end, steps):
        Ab = self._prepare_matrix(self.n + self.m + 1, self._mu, self._lambda)
        time = np.linspace(0, end, steps)
        MA = np.copy(self.A0)
        p = np.copy(self.A0)
        for i in range(steps-1):
            p = p + self._deriv(p, time[i], Ab)*(end/steps)
            MA = np.vstack((MA, p))
        # MA = odeint(self._deriv, self.A0, time, args=(Ab,))
        pp.plot(time, MA, linestyle="-")
        pp.show()
        # print(MA)
        # print(np.sum(MA, axis=1))
        return MA

    @staticmethod
    def _get_state(arr, curr, time, step, max_):
        bound_l = int(curr/step)
        bound_r = bound_l + int(time/step)
        if bound_l >= max_:
            bound_l = max_-1
        if bound_r >= max_:
            bound_r = max_-1
        state = arr[bound_l]
        return state, bound_l, bound_r

    def _realize_model(self, end, count_of_sections):
        requests = np.random.exponential(scale=1/self._lambda, size=end*10)
        time_of_service = np.random.exponential(scale=1/self._mu + 2.3, size=end*10)
        result_raw = np.zeros(count_of_sections)
        step = (end+1)/count_of_sections
        current = 0
        for request, time in np.c_[requests, time_of_service]:
            current += request
            state, bound_l, bound_r = self._get_state(result_raw, current, time, step, count_of_sections)
            if state < self.n + self.m:
                for i in range(bound_l, bound_r):
                    result_raw[i] += 1
            if bound_r == count_of_sections or abs(current - end) < 1:
                self._add_matrix_for_imitation(result_raw)

    def _add_matrix_for_imitation(self, array):
        res = np.zeros((self.n + self.m + 1, array.size))
        for i in range(array.size):
            res[int(array[i])][int(i)] = 1
        self.imitation = np.dstack((self.imitation, res))

    def imitation_modelling(self, end, steps, count_of_sections):
        self.imitation = np.zeros((self.n + self.m + 1, count_of_sections, 1))
        for i in range(steps):
            try:
                self._realize_model(end, count_of_sections)
            except IndexError as e:
                print("index error: {}".format(e))
        result = np.average(self.imitation, axis=2)
        time = np.linspace(0, end, count_of_sections)
        pp.plot(time, np.transpose(result), linestyle="-")
        pp.show()