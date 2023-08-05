REQUIRE_EMAIL = False

UNIQUE_EMAIL = False

ALLOW_PASSWORD_RESET = False

ALLOW_VERIFICATION = False

RESTRICT_UNAUTHENTICATED_USER_ACCESS = False

LOGIN_REQUIRED_EXEMPT_URLS = [
    'accounts/register/',
    'accounts/login/',
    'accounts/verify/',
    'accounts/resend-verification/',
    'accounts/password-reset/',
    'accounts/password-reset/done/',
    'accounts/password-reset/confirm/',
    'accounts/password-reset/complete/',
]

UNAUTHENTICATED_SPECIFIC_URLS = [
    'accounts/register/',
    'accounts/login/',
    'accounts/verify/',
    'accounts/resend-verification/',
]