team1_num = 5
team2_num = 6
score1 = 40
score2 = 42
team1_time = 1552.512
team2_time = 2153.31451
tasks_total = 82

time_avg = (team1_time + team2_time) / tasks_total

if score1 > score2 or score1 == score2 and team1_time > team2_time:
    challenge_result = 'Победа команды Мастера кода!'
elif score1 < score2 or score1 == score2 and team1_time < team2_time:
    challenge_result = 'Победа команды Волшебники данных!'
else:
    challenge_result = 'Ничья!'

# %
print('В команде "Мастера кода" участников: %s!' % team1_num)
print('Итого сегодня в командах участников: %(team1)s и %(team2)s!' % {"team1": team1_num, "team2": team2_num})

# format()
print('Команда "Волшебники данных" решила задач: {score}!'.format(score=score2))
print('"Волшебники данных" решили задачи за {} сек.!'.format(team2_time))

# f-строки
print(f'Команды решили {score1} и {score2} задач')
print(f'Результат битвы: {challenge_result}')
print(f'Сегодня было решено {tasks_total} задач, в среднем по {time_avg:.1f} секунды на задачу!')
