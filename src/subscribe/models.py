from django.db      import models


class Subscribe(models.Model):
    email        = models.CharField(max_length = 200)
    name         = models.CharField(max_length = 200)
    is_subscribe = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True) 
       

    def __str__(self):
        return self.email
   
    class Meta:
        db_table = 'subcribes'
