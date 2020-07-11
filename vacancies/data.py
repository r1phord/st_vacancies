""" Вакансии """

jobs = [

    {"title": "Разработчик на Python", "cat": "backend", "skills": "Python • Git • PostgreSQL",
     "company": "staffingsmarter", "salary_from": "100000",
     "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Разработчик в проект на Django", "cat": "backend", "skills": "Python • Django • Git • PostgreSQL",
     "company": "swiftattack", "salary_from": "80000",
     "salary_to": "90000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Разработчик на Swift в аутсорс компанию", "cat": "backend", "skills": "Swift • Objective-C • Git",
     "company": "swiftattack",
     "salary_from": "120000", "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Мидл программист на Python", "cat": "backend", "skills": "Middle • Python • Git • SQL",
     "company": "workiro",
     "salary_from": "80000",
     "salary_to": "90000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Питонист в стартап", "cat": "backend", "skills": "Python • Flask • Git", "company": "primalassault",
     "salary_from": "120000",
     "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"}

]

""" Компании """

companies = [

    {"name": "workiro", "location": "Москва"},
    {"name": "rebelrage", "location": "Москва"},
    {"name": "staffingsmarter", "location": "Рязань"},
    {"name": "evilthreat h", "location": "Москва"},
    {"name": "hirey ", "location": "Калининград"},
    {"name": "swiftattack", "location": "Екатеринбург"},
    {"name": "troller", "location": "Санкт-Петербург"},
    {"name": "primalassault", "location": "Санкт-Петербург"}

]

""" Категории """

specialties = [

    {"code": "frontend", "title": "Фронтенд"},
    {"code": "backend", "title": "Бэкенд"},
    {"code": "gamedev", "title": "Геймдев"},
    {"code": "devops", "title": "Девопс"},
    {"code": "design", "title": "Дизайн"},
    {"code": "products", "title": "Продукты"},
    {"code": "management", "title": "Менеджмент"},
    {"code": "testing", "title": "Тестирование"}

]

""" Статусы в формате Enum """

#
#
# class EducationChoices(Enum):
#     missing = 'Отсутствует'
#     secondary = 'Среднее'
#     vocational = 'Средне-специальное'
#     incomplete_higher = 'Неполное высшее'
#     higher = 'Высшее'
#
#
# class GradeChoices(Enum):
#     intern = 'intern'
#     junior = 'junior'
#     middle = 'middle'
#     senior = 'senior'
#     lead = 'lead'
#
#
# class SpecialtyChoices(Enum):
#     frontend = 'Фронтенд'
#     backend = 'Бэкенд'
#     gamedev = 'Геймдев'
#     devops = 'Девопс'
#     design = 'Дизайн'
#     products = 'Продукты'
#     management = 'Менеджмент'
#     testing = 'Тестирование'
#
#
# class WorkStatusChoices(Enum):
#     not_in_search = 'Не ищу работу'
#     consideration = 'Рассматриваю предложения'
#     in_search = 'Ищу работу'
