# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save, post_delete
import django.utils.timezone as timezone


# Create your models here.
class Notification(models.Model):
    id = models.IntegerField(primary_key=True)                  # 数据库中的编号
    sender = models.CharField(max_length=256)
    senderId = models.IntegerField(default=0) # 发信用户id
    target = models.IntegerField(default=0)                     # 用户的数据库编号
    title = models.CharField(max_length=256)         # 站内信标题
    content = models.TextField(default=u"暂无简介")             # 信息
    isRead = models.BooleanField(default=False)             # 是否已读
    createTime = models.DateTimeField(default=timezone.now)      # 发信时间
    welcome = models.BooleanField(default=False)

    #  def decr_notifications_counter(sender, instance, **kwargs):
    #    # 当删除的消息还没有被读过时，计数器 -1
    #    if not instance.has_readed:
    #      NotificationController(instance.user_id).update_unread_count(-1)

    #  post_delete.connect(decr_notifications_counter, sender=Notification)

    def __str__(self):
        return '<Notification %s: %s %s %s %s %s %s>' % (self.id,
                                                         self.sender, self.target, self.title,
                                                         self.content, self.isRead, self.createTime)


class NotificationController(models.Model):
    id = models.IntegerField(primary_key=True)  # 数据库中的编号
    userId = models.IntegerField(default=0)  # 用户的数据库编号
    unReadCount = models.IntegerField(default=1)  # 未读条数

    #  def mark_as_readed(self, notification_id):
    #      affected_rows = Notification.objects.filter(pk=notification_id,
    #              has_readed=False).update(has_readed=True)
    #      # affected_rows将会返回update语句修改的条目数
    #      self.update_unread_count(affected_rows)

    def __str__(self):
        return '<NotificationController %s: %s %s>' % (self.id, self.userId, self.unReadCount)
