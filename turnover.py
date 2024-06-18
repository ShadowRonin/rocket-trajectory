def calc_angle(y, system):
    turnover_time, turnover_angle = system.turnover_time, system.turnover_angle

    if y >= turnover_time:
        return turnover_angle
    return 90