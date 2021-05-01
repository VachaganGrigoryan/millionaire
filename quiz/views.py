from random import sample
from uuid import uuid4

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template import loader

from quiz.models import Quiz, Question


@login_required(login_url='/login')
def new_game(request):
    quiz = Quiz.objects.filter(user=request.user, status=Quiz.QuizStatus.in_progress).first()
    if quiz:
        return redirect('game', title=quiz.title)

    questions = Question.objects.all()
    try:
        random_questions = sample(list(questions), k=5)
    except ValueError:
        template = loader.get_template('index.html')
        context = {
            'message': 'Անբավարար հարցեր!',
            'quizzes': quiz
        }
        return HttpResponse(template.render(context, request))

    new_quiz = Quiz.objects.create(user=request.user, title=str(uuid4()).upper())
    new_quiz.set_questions(random_questions)

    return HttpResponseRedirect(f'/millionaire/game/{new_quiz.title}')


@login_required(login_url='/login')
def game(request, title):
    quiz = get_object_or_404(
        Quiz,
        user=request.user,
        title=title,
        status=Quiz.QuizStatus.in_progress
    )
    question = quiz.get_next_question()

    if question is None:
        quiz.set_status(Quiz.QuizStatus.done)
        return redirect('score', title=title)

    template = loader.get_template('quiz/quiz.html')
    context = {
        'quiz': quiz,
        'question': question
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='/login')
def answer(request, title):
    if request.method != 'POST':
        return redirect('game', title=title)

    question_id = request.POST.get('question')
    answer = request.POST.get('answer')

    if not question_id or not answer:
        return redirect('game', title=title)

    quiz = get_object_or_404(
        Quiz,
        user=request.user,
        title=title,
        questions__id=question_id,
        questions__options__body=answer
    )

    quiz_answer = quiz.election(question_id, answer)

    template = loader.get_template('quiz/answer.html')
    context = {
        'answer': quiz_answer
    }
    return HttpResponse(template.render(context, request))


def score(request, title):
    quiz = get_object_or_404(
        Quiz,
        user=request.user,
        title=title,
        status__in=(Quiz.QuizStatus.done, Quiz.QuizStatus.closed)
    )
    template = loader.get_template('quiz/score.html')
    context = {
        'quiz': quiz
    }
    return HttpResponse(template.render(context, request))


def close(request, title):
    quiz = get_object_or_404(
        Quiz,
        user=request.user,
        title=title
    )
    quiz.set_status(Quiz.QuizStatus.closed)
    return redirect('home')
