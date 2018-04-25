# -*- coding: utf-8 -*-


def pretty_output(method):
    def wrapped(pretty_output=False):
        res = method()
        if pretty_output:
            print("{}: {}".format(method.__doc__, res))
        return res
    return wrapped


class Problem():
    def __init__(self, request_time, service_time, queue_max, name="Задача 5.1"):
        """ Одноканальная СМО с ожиданием и ограничением на длину очереди
        Этот класс реализует методы описанные в таблице 5.2(на стр 80-82)
         Л.Г ЛАБСКЕР, Л.О. БАБЕШКО "Теория массового обслуживания в экономической сфере" """
        self.name = name
        self._lambda = 1 / request_time
        self._mu = 1 / service_time
        self._m = queue_max
        self._p_via_ro = list()
        self._p_via_T = list()
        self._ro = self._lambda / self._mu
        self._T_service = service_time
        self._T = request_time
        self._add_pretty_output()

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


