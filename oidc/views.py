from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url, redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View

from oidc.registry import oauth

REDIRECT_FIELD_NAME = 'next'


class LoginView(View):
    """Redirects to authorize endpoint of OpenID Connect provider."""

    def get(self, request, *args, **kwargs):
        redirect_uri = request.build_absolute_uri(reverse('oidc:auth'))
        return oauth.keycloak.authorize_redirect(request, redirect_uri)


class AuthView(View):
    """Processes response from the OpenID Connect provider."""

    def get_user(self, id_token):
        """Get Django user from ID token.

        Returns:
            The user if found, else None.
        """
        username = id_token['preferred_username']
        user_model = get_user_model()
        try:
            return user_model.objects.get(username__iexact=username)
        except user_model.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        # Get and parse access token + ID token
        token = oauth.keycloak.authorize_access_token(request)
        id_token = oauth.keycloak.parse_id_token(request, token)
        # Retrieve user
        user = self.get_user(id_token)
        if user is None:
            raise PermissionDenied
        # Log the user in
        login(request, user)
        return redirect('index')
        # return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.GET.get(REDIRECT_FIELD_NAME, '')
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts={self.request.as_host()},
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''
