from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class AcsPhone(models.Model):
    acs_id = models.IntegerField('ID конференции', unique=True,
                                 help_text='ID конференции на АКСС')
    phone = models.IntegerField('Номер конференции', unique=True,
                                blank=False, null=False, validators=[
                                    MinValueValidator(33300),
                                    MaxValueValidator(33399)],
                                help_text='5-значный внутренний номер')
    password = models.IntegerField('ПИН-код конференции', blank=False,
                                   null=False, validators=[
                                       MinValueValidator(0000),
                                       MaxValueValidator(9999)],
                                   help_text='ПИН-код от номера на АКСС')

    class Meta:
        verbose_name = 'АКС Номер'
        verbose_name_plural = 'АКС Номера'
        default_related_name = 'acs_phones'
        constraints = [
            models.UniqueConstraint(
                fields=('acs_id', 'phone'),
                name='Ограничение по уникальному номеру АКС'
            )
        ]

    def __str__(self):
        return self.phone


class BookingAcs(models.Model):
    acs_phone = models.ForeignKey(AcsPhone, on_delete=models.CASCADE,
                                  verbose_name='АКС Номер')
    start_conf = models.DateTimeField('Время начала конференции')
    end_conf = models.DateTimeField('Время окончания конференции')
    owner = models.ForeignKey(User, verbose_name='Владелец бронирования',
                              on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'bookings'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(start_conf__lt=models.F('end_conf')),
                name='Начало до окончания'
            ),
            # models.CheckConstraint(
            #     condition=models.Q(start_conf__lt=models.F('end_conf')),
            #     name='Начало до окончания'
            # )
        ]

    def __str__(self):
        return f'Бронь {self.owner} номера {self.acs_phone}'
