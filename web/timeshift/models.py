from django.db import models


class City(models.Model):
    """
    {'datetime': '2023-02-11 12:33:16',
    'timezone_name': 'Moscow Standard Time',
    'timezone_location': 'Europe/Moscow',
    'timezone_abbreviation': 'MSK',
    'gmt_offset': 3, 'is_dst': False,
    'requested_location': 'москва',
    'latitude': 55.7504461,
    'longitude': 37.6174943
    }

    """
    name = models.CharField(max_length=200)
    gmt_offset = models.IntegerField()
    created_time = models.DateTimeField()

    def __str__(self):
        return f'{self.name}, offset - {self.gmt_offset}'

    class Meta:
        ordering = ('name', )
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
