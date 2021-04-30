from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import loader

from random import sample
from uuid import uuid4

from quiz.models import Quiz, Question


@login_required(login_url='/login')
def new_game(request):
    quiz = Quiz.objects.filter(user=request.user, status=Quiz.QuizStatus.in_progress).first()
    if quiz:
        return redirect('game', title=quiz.title)

    questions = Question.objects.all()
    random_questions = sample(list(questions), k=5)

    new_quiz = Quiz.objects.create(user=request.user, title=str(uuid4()).upper())
    new_quiz.questions.set(random_questions)
    new_quiz.save()

    template = loader.get_template('quiz/quiz.html')
    context = {
        'quiz': new_quiz,
        'question': new_quiz.questions.first()
    }

    return HttpResponseRedirect(f'/millionaire/game/{new_quiz.title}', content=template.render(context, request))


@login_required(login_url='/login')
def game(request, title):
    quiz = Quiz.objects.filter(user=request.user, title=title, status=Quiz.QuizStatus.in_progress).first()

    if quiz is None:
        return redirect('/')

    question = quiz.questions.first()
    answer = quiz.is_answered_question(question_id=question.id)

    template = loader.get_template('quiz/quiz.html')
    context = {
        'quiz': quiz,
        'question': question,
        'answer': answer
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='/login')
def answer(request, title):
    if request.method != 'POST':
        return redirect('/')

    question_id = request.POST.get('question')
    answer = request.POST.get('answer')

    if question_id and answer:
        quiz = Quiz.objects.filter(
            user=request.user,
            title=title,
            status=Quiz.QuizStatus.in_progress,
            questions__id=question_id
        ).first()

        if quiz and not quiz.is_answered_question(question_id):
            quiz_answer = quiz.election(question_id, answer)
            if quiz_answer:
                template = loader.get_template('quiz/quiz.html')
                context = {
                    'quiz': quiz_answer.quiz,
                    'question': quiz_answer.question,
                    'answer': quiz_answer.selected
                }
                return HttpResponseRedirect(f'/millionaire/game/{title}', content=template.render(context, request))

    return redirect('game', title=title)