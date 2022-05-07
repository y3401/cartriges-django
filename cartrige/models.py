from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User  # Required to assign User as a borrower
from django.core.validators import validate_image_file_extension
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField

class MetaCart(models.Model):
    metatitle = models.CharField(max_length=40,verbose_name='Наименование группы', unique=True, help_text="")
    
    def __str__(self):
        return self.metatitle

    class Meta:
        ordering = ['metatitle']
        verbose_name_plural = "Группы картриджей"

class Cartriges(models.Model):
    name_cart = models.CharField(max_length=50, help_text="", verbose_name="Картридж", unique=True)
    photo = models.ImageField(upload_to='images/', validators=[FileExtensionValidator], null=True, blank=True, verbose_name="Фото")
    comment = models.TextField(max_length=300, null=True, blank=True, help_text="", verbose_name="Примечание")
    metacart = models.ForeignKey(MetaCart, on_delete=models.PROTECT, null=True, verbose_name="Группа")
    
    def __str__(self):
        return self.name_cart

    class Meta:
        ordering = ['name_cart']
        verbose_name_plural = "Модели картриджей"



class Printers(models.Model):
    name_printer = models.CharField(max_length=100, help_text="", verbose_name="Принтер", unique=True)
    photo_prn = models.ImageField(upload_to='images/', validators=[FileExtensionValidator], null=True, blank=True, verbose_name="Фото")
    cart = models.ManyToManyField(Cartriges, related_name="carts", blank=True, verbose_name="Совместимые картриджи")
    
    def __str__(self):
        return '{0}'.format(self.name_printer)
    class Meta:
        ordering = ['name_printer']
        verbose_name_plural = "Модели принтеров"

class Sklad(models.Model):
    cartriges = models.ForeignKey('Cartriges', on_delete=models.PROTECT, null=True, verbose_name="Картридж")
    cart_buh = models.CharField(max_length=255, help_text="", verbose_name="Картридж по бухгалтерии", unique=True)
    cart_count = models.IntegerField(verbose_name="Количество", default=0)
    
    def __str__(self):
        return self.cart_buh


    class Meta:
        ordering = ['cartriges',]
        verbose_name_plural = 'Склад'

class Depart(models.Model):
    name_depart = models.CharField(max_length=100, help_text="", verbose_name="Наименование подразделения", unique=True)
    fio = models.CharField(max_length=40, help_text="", verbose_name="Начальник/Ответственный",blank=True)
    adm = models.BooleanField(default=False, verbose_name="Отдел IT")
    
    def __str__(self):
        return '{0}'.format(self.name_depart)
    
    class Meta:
        ordering = ['name_depart']
        verbose_name_plural = 'Подразделения'

class ContrAgent(models.Model):
    name_agent = models.CharField(max_length=50, help_text="", verbose_name="Краткое наименование", unique=True)
    name_agent_full = models.CharField(max_length=150, help_text="", verbose_name="Полное наименование")
    fio_nach = models.CharField(max_length=40, help_text="", verbose_name="Руководитель",blank=True)
    nach_dolj = models.CharField(max_length=40, help_text="", verbose_name="Должность руководителя",blank=True)
    fio_zam = models.CharField(max_length=40, help_text="", verbose_name="Зам.руководителя",blank=True)
    inn = models.CharField(max_length=100, help_text="", verbose_name="ИНН, КПП, ОГРН и т.д.",blank=True)
    address = models.CharField(max_length=100, help_text="", verbose_name="Адрес",blank=True)
    email = models.EmailField(max_length=30,help_text="", verbose_name="Е-майл", blank=True)
    phone = PhoneNumberField(verbose_name="Телефон", blank=True)
    otvet = models.CharField(max_length=25, help_text="", verbose_name="Приемщик",blank=True)
    adm = models.BooleanField(default=False, verbose_name="Наша организация")
    def __str__(self):
        return '{0}'.format(self.name_agent)
    
    class Meta:
        ordering = ['name_agent']
        verbose_name_plural = 'Контрагент'

class AllPrinters(models.Model):
    inventar_num = models.CharField(max_length=10, verbose_name="Серийный номер",unique=True)
    printer_model = models.ForeignKey('Printers',verbose_name='Модель принтера',on_delete=models.SET_NULL,null=True)
    dep = models.ForeignKey('Depart',verbose_name='Подразделение',on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '{0} ({1})'.format(self.inventar_num, self.printer_model)
    
    class Meta:
        ordering = ['printer_model']
        verbose_name_plural = 'Принтеры организации'

class Nmax(models.Model):
    zapis = models.IntegerField(default=0)
    nmax = models.IntegerField(verbose_name="Текущий максимальный номер картриджа")
    def __str__(self):
        return str(self.nmax)
    class Meta:
        verbose_name_plural = 'Максимальный номер'


class Records(models.Model):
    inventar = models.IntegerField(null=True, verbose_name="Учетный N", unique=True)
    id_cart = models.ForeignKey('Cartriges', on_delete=models.PROTECT, null=True, verbose_name="Картридж")
    id_dep = models.ForeignKey('Depart', on_delete=models.PROTECT, null=True, verbose_name="Подразделение")
    charge_num = models.IntegerField(default=1, verbose_name="Количество заправок")
   
    LOAN_STATUS = (
        (1, 'Новый'),
        (2, 'Установлен'),
        (3, 'Пустой'),
        (4, 'Заправка'),
        (5, 'Заправлен'),
        (6, 'Дефект'),
        (7, 'Списан'),
    )

    #REASON = (
    #    (1,'Износ'),
    #    (2,'Поломка'),
    #    (3,'Устаревание'),
    #)

    status = models.PositiveSmallIntegerField(choices=LOAN_STATUS, default=5, help_text='Статус картриджа', verbose_name="Статус")
    date_in = models.DateField(null=True, blank=True, verbose_name="Дата ввода в эксплуатацию", auto_now=True, auto_created=True, editable=False)
    date_out = models.DateField(null=True, blank=True, verbose_name="Дата передачи/списания")
    comment = models.TextField(max_length=300, blank=True, null=True, help_text="Комментарий", verbose_name="Комментарий")
    c_agent = models.ForeignKey('ContrAgent', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Контрагент")
    tkn = models.CharField(max_length=32, verbose_name="Токен", blank=True, null=True, unique=True)
    #reason = models.TextField(max_length=150, null=True, blank=True, help_text="Причина списания", verbose_name="Причина списания")
    #reason = models.PositiveSmallIntegerField(choices=REASON, blank=True, default=0, help_text='Причина', verbose_name="Причина")
    #docum = models.TextField(max_length=75, null=True, blank=True, help_text="Документ", verbose_name="Документ-основание")

    def __str__(self):
        return str(self.inventar)
    class Meta:
        ordering = ['inventar']
        verbose_name_plural = "Учет"

class Operation(models.Model):
    kod = models.IntegerField(verbose_name="Код операции")
    operation_name = models.CharField(max_length=25, verbose_name="Операция")
    class Meta:
        verbose_name_plural = "Операции"
    def __str__(self):
        return str(self.operation_name)

class Logs(models.Model):

    date_event = models.DateTimeField(verbose_name="Дата и время события", null=True, blank=True, editable=False)
    token = models.CharField(max_length=32, verbose_name="Токен",unique=True)
    name_user = models.CharField(max_length=15, verbose_name="Пользователь")
    action = models.ForeignKey('Operation', on_delete=models.SET_NULL, null=True, verbose_name="Операция")
    obj = models.ForeignKey('Records', on_delete=models.SET_NULL, null=True, verbose_name="ID_объекта")
    #obj = models.IntegerField(verbose_name="ID объекта")
    izm = models.CharField(max_length=300, verbose_name="Подробно", blank=True, null=True)
    dep = models.IntegerField(verbose_name="ID подразделения", null=True)

    class Meta:
        ordering = ['-date_event']
        verbose_name_plural = "Логи"

class Tmp(models.Model):
    god = models.IntegerField(default=2022)
    meta = models.CharField(max_length=50, blank=True, null=True)
    oper = models.CharField(max_length=50, blank=True, null=True)
    actid = models.IntegerField(default=0)
    m1 = models.IntegerField(default=0)
    m2 = models.IntegerField(default=0)
    m3 = models.IntegerField(default=0)
    m4 = models.IntegerField(default=0)
    m5 = models.IntegerField(default=0)
    m6 = models.IntegerField(default=0)
    m7 = models.IntegerField(default=0)
    m8 = models.IntegerField(default=0)
    m9 = models.IntegerField(default=0)
    m10 = models.IntegerField(default=0)
    m11 = models.IntegerField(default=0)
    m12 = models.IntegerField(default=0)
    msum = models.IntegerField(default=0)
    ord = models.IntegerField(default=0)