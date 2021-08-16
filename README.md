# shakespeare_plays_project

Example of MongoDB usage in python app

-----------------УСЛОВИЯ ЗАДАЧИ----------------------------------

Датасет содержит 36 пьес Уильяма Шекспира.

Каждый документ пьесы содержит в себе коллекцию актов, состощих из сцен, каждая сцена содержит коллекцию реплик, разбитых на предложения например:

{
    "_id" : "Romeo and Juliet",
    "acts" : [ 
        {
            "title" : "ACT I",
            "scenes" : [ 
                {
                    "title" : "SCENE I. Verona. A public place.",
                    "action" : [ 
                        {
                            "character" : "SAMPSON",
                            "says" : [ 
                                "Gregory, o' my word, we'll not carry coals."
                            ]
                        }, 
                        {
                            "character" : "GREGORY",
                            "says" : [ 
                                "No, for then we should be colliers."
                            ]
                        }, 
						// ...
                        {
                            "character" : "GREGORY",
                            "says" : [ 
                                "To move is to stir; and to be valiant is to stand:", 
                                "therefore, if thou art moved, thou runn'st away."
                            ]
                        }, 
                        {
                            "character" : "SAMPSON",
                            "says" : [ 
                                "A dog of that house shall move me to stand: I will", 
                                "take the wall of any man or maid of Montague's."
                            ]
                        }, 
                        {
                            "character" : "GREGORY",
                            "says" : [ 
                                "That shows thee a weak slave; for the weakest goes", 
                                "to the wall."
                            ]
                        }, 
						// ...
				},
				// ...
			]
		},
		// ...
	]
}

----------------------------------------------------
Задачи:

- Найдите сцену с самым большим количеством реплик в сцене (надо указать название пьесы, акт и сцену);
- Какие персонажи встречаются больше чем в одной пьесе?

-------------------ОПИСАНИЕ РЕШЕНИЯ--------------------------------

Mongo запускается в docker-е, база и колекция заполняется через скрипт инициализации при старте контейнера.

Шаги для запуска приложения:

1. В 1-ом окне терминала выполнить скрипт up_environment.sh;
2. Во 2ом окне терминала запустить скрипт run_app.sh.

-------------------ПРОЧЕЕ------------------------------------------

- up_environment.sh - создает и запускает среду в докере
- run_app.sh - запускает консольное приложение
- docker/mongo/shakespeare_plays.json - датасет с пьесами
- docker/mongo/init_mongo.sh - скрипт импортирующий датасет
- dev.env - переменные среды

