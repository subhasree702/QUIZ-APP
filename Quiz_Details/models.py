# from django.db import models

# class Topic(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name


# class Question(models.Model):
#     topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
#     question_text = models.TextField(max_length=300)
#     option1 = models.CharField(max_length=200)
#     option2 = models.CharField(max_length=200)
#     option3 = models.CharField(max_length=200)
#     option4 = models.CharField(max_length=200)
#     correct_answer = models.CharField(max_length=200)

#     def __str__(self):
#         return self.question_text


# from django.db import models
# from django.contrib.auth.models import User

# class Topic(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name


# class Question(models.Model):
#     topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
#     question_text = models.TextField(max_length=300)
#     option1 = models.CharField(max_length=200)
#     option2 = models.CharField(max_length=200)
#     option3 = models.CharField(max_length=200)
#     option4 = models.CharField(max_length=200)
#     correct_answer = models.CharField(max_length=200)
#     level = models.IntegerField(default=1) 

#     def __str__(self):
#         return f"{self.question_text} (Level {self.level})"


# class UserProgress(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
#     current_level = models.IntegerField(default=1)
#     highest_score = models.FloatField(default=0)

#     def __str__(self):
#         return f"{self.user.username} - {self.topic.name} (Level {self.current_level})"
from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    question_text = models.TextField(max_length=300)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=200)
    level = models.IntegerField(default=1)  # 1=Basic, 2=Intermediate, etc.

    def __str__(self):
        return f"{self.question_text} (Level {self.level})"


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    current_level = models.IntegerField(default=1)
    highest_score = models.FloatField(default=0)

    # ✅ Add these two fields
    passed_level1 = models.BooleanField(default=False)
    passed_level2 = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.topic.name} (Level {self.current_level})"
