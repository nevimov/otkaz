from django.contrib.admin.sites import AdminSite


class MainAdminSite(AdminSite):
    site_header = 'Административный сайт «отказные‑окна.рф»'
    site_title = 'Административный сайт'
    index_title = 'Главная страница'

main_admin_site = MainAdminSite('main-admin')

def get_main_adminsite():
    return main_admin_site