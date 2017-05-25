from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse, HttpResponseGone
from django.shortcuts import redirect

from .django_openidauth import views as django_openidauth_views
from .django_openidconsumer import views as django_openidconsumer_views
from .djangopeople import views, api


def perm_redirect(url):
    return lambda req: redirect(url, permanent=True)


favicon = perm_redirect(
    '%sdjangopeople/img/favicon.ico' % settings.STATIC_URL
)


def robots(request):
    return HttpResponse('User-agent: *\nDisallow:\n', content_type='text/plain')


def gone(request):
    return HttpResponseGone()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^about/$', views.about, name='about'),
    url(r'^recent/$', views.recent, name='recent'),

    url(r'^recover/$', views.recover, name='password_reset_recover'),
    url(r'^', include('password_reset.urls')),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^geonames/$', views.geonames, name='geonames'),

    url(r'^favicon.ico$', favicon),
    url(r'^robots.txt$', robots, name='robots'),
    url(r'^static/profiles/_thumbs/.*', gone, name='gone'),
    url(r'^static/img/.*', gone),

    # openid stuff
    url(
        r'^openid/$', django_openidconsumer_views.begin, {
            'sreg': 'email,nickname,fullname',
            'redirect_to': '/openid/complete/',
        }, name='openid_begin'),
    url(r'^openid/complete/$',
        django_openidconsumer_views.complete,
        name='openid_complete'),

    url(r'^openid/whatnext/$', views.openid_whatnext, name='openid_whatnext'),

    url(r'^openid/signout/$', django_openidconsumer_views.signout, name='openid_signout'),

    url(r'^openid/associations/$', django_openidauth_views.associations,
        name='openid_associations'),

    url(r'^search/$', views.search, name='search'),

    url(r'^skills/(?P<tag>.*)/$', views.skill, name='skill_detail'),
    url(r'^skills/$', views.skill_cloud, name='skill_cloud'),

    url(r'^api/stats/$', api.stats, name='stats'),

    url(r'^api/irc_lookup/(.*?)/$', api.irc_lookup, name='irc_lookup'),
    url(r'^api/irc_spotted/(.*?)/$', api.irc_spotted, name='irc_spotted'),
    url(r'^irc/active/$', views.irc_active, name='irc_active'),
    url(r'^irc/(.*?)/$', api.irc_redirect, name='irc_redirect'),

    url(r'^uk/$', perm_redirect('/gb/')),

    url(r'^(?P<country_code>[a-z]{2})/$',
        views.country, name='country_detail'),

    url(r'^(?P<country_code>[a-z]{2})/sites/$',
        views.country_sites, name='country_sites'),

    url(r'^(?P<country_code>[a-z]{2})/skills/$',
        views.country_skill_cloud, name='country_skill_cloud'),

    url(r'^(?P<country_code>[a-z]{2})/skills/(?P<tag>.*)/$',
        views.country_skill, name='country_skill'),

    url(r'^(?P<country_code>[a-z]{2})/looking-for/(?P<looking_for>freelance|full-time)/$',  # noqa
        views.country_looking_for, name='country_looking_for'),

    url(r'^(?P<country_code>[a-z]{2})/(?P<region_code>\w+)/$',
        views.region, name='country_region'),

    url(r'^profile/', views.redirect_to_logged_in_user_profile,
        name='redirect_to_logged_in_user_profile'),

    url(r'^(?P<username>[a-z0-9]{3,})/$', views.profile, name='user_profile'),
    url(r'^(?P<username>[a-z0-9]{3,})/bio/$', views.edit_bio, name='edit_bio'),
    url(r'^(?P<username>[a-z0-9]{3,})/skills/$',
        views.edit_skills, name='edit_skills'),

    url(r'^(?P<username>[a-z0-9]{3,})/password/$',
        views.edit_password, name='edit_password'),

    url(r'^(?P<username>[a-z0-9]{3,})/account/$',
        views.edit_account, name='edit_account'),

    url(r'^(?P<username>[a-z0-9]{3,})/portfolio/$',
        views.edit_portfolio, name='edit_portfolio'),

    url(r'^(?P<username>[a-z0-9]{3,})/location/$',
        views.edit_location, name='edit_location'),

    url(r'^(?P<username>[a-z0-9]{3,})/finding/$',
        views.edit_finding, name='edit_finding'),

    url(r'^(?P<username>[a-z0-9]{3,})/delete/$',
        views.delete_account_request, name='delete_account_request'),

    url(r'^(?P<username>[a-z0-9]{3,})/delete/next/$',
        views.delete_account_next, name='delete_account_next'),

    url(r'^(?P<username>[a-z0-9]{3,})/delete/done/$',
        views.delete_account_done, name='delete_account_done'),

    url(r'^(?P<username>[a-z0-9]{3,})/delete/(?P<key>.+)/$',
        views.delete_account, name='delete_account'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
