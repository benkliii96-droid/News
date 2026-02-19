from django.contrib.auth.models import User
from newsapp.models import Author, Category, Post, Comment

user1 = User.objects.create_user('user1')
user2 = User.objects.create_user('user2')

author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

cat_sport = Category.objects.create(name='Спорт')
cat_politics = Category.objects.create(name='Политика')
cat_tech = Category.objects.create(name='Технологии')
cat_culture = Category.objects.create(name='Культура')

post1 = Post.objects.create(
    author=author1,
    post_type=Post.ARTICLE,
    title='Научная статья о спорте',
    content='Спорт играет важную роль в жизни современного общества. Он не только укрепляет здоровье, но и способствует развитию командного духа. В данной статье мы рассмотрим последние научные исследования в области физической культуры и их влияние на продолжительность жизни. Ученые из разных стран пришли к выводу, что регулярные умеренные нагрузки снижают риск сердечно-сосудистых заболеваний на 30%. Также обсуждается вопрос о том, какие виды спорта наиболее эффективны для поддержания тонуса и какие существуют программы тренировок для разных возрастных групп.'
)
post2 = Post.objects.create(
    author=author2,
    post_type=Post.ARTICLE,
    title='Анализ политической ситуации',
    content='Политическая ситуация в мире постоянно меняется. В последние годы мы наблюдаем усиление напряженности между ведущими державами. Аналитики спорят о причинах и возможных последствиях этих процессов. В этой статье мы попытаемся разобраться в текущих тенденциях и дать прогноз на ближайшее будущее. Особое внимание уделяется экономическим санкциям, их влиянию на глобальную торговлю и попыткам найти дипломатические решения. Рассматриваются также внутренние политические изменения в ключевых странах и их возможное отражение на международной арене.'
)
post3 = Post.objects.create(
    author=author1,
    post_type=Post.NEWS,
    title='Новость: открытие нового технопарка',
    content='Вчера в нашем городе состоялось торжественное открытие нового технопарка. Это событие собрало множество гостей, включая представителей власти и бизнеса. Технопарк оснащен современным оборудованием и будет способствовать развитию инновационных проектов. Планируется, что он станет площадкой для стартапов и научных исследований. На церемонии выступили глава региона и руководители крупных IT-компаний, которые выразили готовность поддерживать резидентов технопарка. Уже сейчас несколько молодых команд представили свои проекты в области искусственного интеллекта и робототехники. Ожидается, что технопарк создаст более 500 новых рабочих мест и привлечет инвестиции в регион.'
)

post1.category.add(cat_sport, cat_tech)
post2.category.add(cat_politics)
post3.category.add(cat_tech, cat_culture)

comment1 = Comment.objects.create(
    post=post1,
    userComment=user1,
    content='Интересная статья!'
)
comment2 = Comment.objects.create(
    post=post1,
    userComment=user2,
    content='Спасибо за информацию.'
)
comment3 = Comment.objects.create(
    post=post2,
    userComment=user1,
    content='Не согласен с выводами.'
)
comment4 = Comment.objects.create(
    post=post3,
    userComment=user2,
    content='Когда откроют в нашем городе?'
)

post1.like()
post1.like()
post1.dislike()
post2.like()
post3.like()
post3.like()
post3.like()

comment1.like()
comment1.like()
comment2.dislike()
comment3.like()
comment3.like()
comment4.like()
comment4.like()
comment4.like()

author1.update_rating()
author2.update_rating()

best_author = Author.objects.order_by('-author_rating').first()
print(f"Лучший автор: {best_author.user.username}, рейтинг: {best_author.author_rating}")

best_post = Post.objects.order_by('-postRating').first()
print(f"Дата: {best_post.date}")
print(f"Автор: {best_post.author.user.username}")
print(f"Рейтинг статьи: {best_post.postRating}")
print(f"Заголовок: {best_post.title}")
print(f"Превью: {best_post.preview()}")

comments_to_best = Comment.objects.filter(post=best_post).order_by('date')
print(f"Комментарии к статье «{best_post.title}»:")
for comment in comments_to_best:
    print(f"{comment.date} | {comment.userComment.username} | рейтинг: {comment.commentRating} | {comment.content}")