from django.contrib.auth.views import LoginView
from django.contrib.sites import requests
from django.core.serializers import json
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings

from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User

from django.views.generic import CreateView
from slack_bot_app.forms import UserForm
from slack_bot_app.models import Team, Message, Thread

from slackclient import SlackClient


def index(request):

    # Team.objects.create(
    #     name='workbot_test',
    #     team_id= "U8B4AM812",
    #     bot_user_id="282559645383.283555506357",
    #     bot_access_token="xoxb-283146722036-v8pYN2wwFJ005hmqhiQo7SM0",
    # )
    print(Team.objects.all())

    return render(request, 'slack_bot_app/index.html', {})


def register(request):
    return render(request, 'slack_bot_app/register.html', {})


class Login(LoginView):
    template_name = 'slack_bot_app/login.html'


class Registration(CreateView):
    template_name = "slack_bot_app/register.html"
    model = User
    form_class = UserForm
    success_url = "/slack_bot/"

    def form_valid(self, form):
        response = super(Registration, self).form_valid(form)
        self.object.set_password(form.cleaned_data['password'])
        self.object.save()
        return response

    def get_context_data(self, **kwargs):
        return super(Registration, self).get_context_data(**kwargs)


# выход из системы
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/slack_bot/')


def slack_oauth(request):
    code = request.GET['code']
    print(code)
    params = {
        'code': code,
        'client_id': "282559645383.283555506357", #settings.SLACK_CLIENT_ID,
        'client_secret': "297245be757f75f5039b7d69aae36845" # settings.SLACK_CLIENT_SECRET
    }
    url = 'https://slack.com/api/oauth.access'
    json_response = requests.get(url, params)
    data = json.loads(json_response.text)
    Team.objects.get_or_create(
        name=data['name'],
        team_id=data['team_id'],
        bot_user_id=data['bot']['bot_user_id'],
        bot_access_token=data['bot']['bot_access_token']
    )
    return redirect('/slack_bot/')


@login_required
def statistics(request, slug):
    messages = Message.objects.filter(team=slug)
    threads = Thread.objects.all()
    return render(request, 'slack_bot_app/stat.html', {'messages': messages, 'threads': threads})


def send_save_message(request):
    req = request.POST
    workspace = Team.objects.get(team_id=req.get('team_id'))
    slack_client = SlackClient(workspace.bot_access_token)
    response = slack_client.api_call(
        'chat.postMessage',
        channel=workspace.channel_id,
        text="П@%s : '%s'" % (req['user_name'], req['text'])
    )
    Message.objects.get_or_create(
            text=response['message']['text'],
            user_id=response['user_id'],
            user_name=response['user_name'],
            team=response['team_id']
        )
    return HttpResponse('Ok')

