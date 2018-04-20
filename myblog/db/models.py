from django.db import models, connections
from django.contrib.auth.models import AbstractUser
from django.db.models import Q, F
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
# Create your models here.


# Table: User
class MyUser(AbstractUser):
    '''
        id INT(11)
        password VARCHAR(128)
        last_login DATETIME(6)
        is_superuser TINYINT(1)
        username VARCHAR(150)
        first_name VARCHAR(30)
        last_name VARCHAR(150)
        email VARCHAR(254)
        is_staff TINYINT(1)
        is_active TINYINT(1)
        date_joined DATETIME(6)
    '''
    mbu_is_login = models.BooleanField(_('Login Status'), default=False)
    mbu_status = models.BooleanField(_('User Status'), default=True)
    mbu_email = models.EmailField(
        _('Email Address'), 
        max_length=100,
        unique=True, 
        help_text=_('Required. 100 characters or fewer. follow in with standard email format.'),
        error_messages={'unique': _("The email address has been registered by another user."),},
    )
    mbu_avatar = models.ImageField(upload_to='uploads/avatars/%Y/%m/%d/%H/%M/%S',
                                   default='uploads/avatars/default_avatar.jpg', verbose_name='Avatar')
    
    class Meta:
        db_table = 'mb_user'
        # unique_together = [("username", "email")]
     
    def __str__(self):
        return "%s (%s)" % (self.username, self.email)


# Table: MB_CATEGORY
class Category(models.Model):
    mbc_id = models.SmallIntegerField('Category ID', primary_key=True)
    mbc_name = models.CharField(
        'Category Name', max_length=20, null=False, blank=False)
    mbc_desc = models.CharField(
        'Category Description', max_length=50, default='')
    # mbc_parent_id = models.SmallIntegerField('Parent Category ID', default=0)
    mbc_parent_id = models.ForeignKey('self', on_delete=models.CASCADE, db_column='mbc_parent_id',
                                      verbose_name='Parent Category ID', related_name='subcategory')
    mbc_order = models.SmallIntegerField(
        'Category Orders', blank=False, default=0)

    def __str__(self):
        return self.mbc_name

    def get_absolute_url(self):
        return reverse('category', args=[self.mbc_id])

    @property
    def has_child(self):
        n = Category.objects.filter(mbc_parent_id=self.mbc_id).count()
        return True if n > 1 else False

    '''
    def get_all_children(self, include_self=False):
        r = []
        if include_self:
            r.append([self.mbc_id,self.mbc_name,self.mbc_order])

        for c in Category.objects.filter(mbc_parent_id=self.mbc_id).exclude(mbc_parent_id=F('mbc_id')):
            r = c.get_all_children(include_self=True)
            if 0 < len(_r):
                r.extend(_r)
        
        return r
    '''

    def get_all_children(self, include_self=False):
        r = []
        if include_self:
            r.append(self)

        for c in Category.objects.filter(mbc_parent_id=self.mbc_id).exclude(mbc_parent_id=F('mbc_id')):
            _r = c.get_all_children(include_self=True)
            if 0 < len(_r):
                r.extend(_r)
        return r

    def get_category_array(self):
        c = [[self.mbc_id, self.mbc_name]]
        # sc = Category.objects.get()
        if self.mbc_parent_id.mbc_id != self.mbc_id:
            sc = self.mbc_parent_id
            _c = sc.get_category_array()
            if 0 < len(_c):
                c.extend(_c)
                # c.append(_c)

        return c

    def get_post_nums_by_category(self):
        p = 0
        ids = []
        c = self.get_all_children(include_self=True)
        for r in c:
            ids.append(r.mbc_id)

        p = Post.objects.filter(mbp_category__in=ids).count()
        return p

    class Meta:
        db_table = 'mb_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['mbc_order']

# Table: MB_POST


class Post(models.Model):
    mbp_id = models.CharField('Post ID', max_length=8, primary_key=True)
    mbp_title = models.CharField('Post Title', max_length=100)
    mbp_summary = models.TextField('Post Summary')
    mbp_content = models.TextField('Post Content')
    mbp_image = models.ImageField(
        'Post Image', upload_to='uploads/postimg/%Y/%m/%d/%H/%M/%S', default='uploads/postimg/default_post.jpg')
    mbp_image_caption = models.CharField(
        'Image Caption', max_length=16, default='')
    # mbp_auther_id = models.models.IntegerField()
    mbp_auther_id = models.ForeignKey(MyUser, to_field='id', on_delete=models.CASCADE,
                                      related_name='auther', db_column='mbp_auther_id', verbose_name='Auther ID')
    mbp_auther = models.CharField('Auther Name', max_length=20)
    mbp_created_at = models.DateTimeField(
        'Post Create DateTime', auto_now_add=True)
    mbp_mod_flag = models.BooleanField('Post modify flag', default=False)
    mbp_last_at = models.DateTimeField(
        'Post last modify datetime', auto_now=True)
    # mbp_last_by_id = models.IntegerField()
    mbp_last_by_id = models.ForeignKey(MyUser, to_field='id', on_delete=models.CASCADE,
                                       related_name='editor', db_column='mbp_last_by_id', verbose_name='Last Modified By')
    mbp_last_by_name = models.CharField('Post last modify name', max_length=20)
    # mbp_category = models.IntegerField('Post Category ID')
    mbp_category = models.ForeignKey(
        Category, to_field='mbc_id', on_delete=models.CASCADE, db_column='mbp_category', verbose_name='Category ID')
    mbp_publish_opt = models.BooleanField('Post publish option', default=True)

    def __setitem__(self, k, v):
        self.k = v

    def __str__(self):
        return self.mbp_id

    def get_all_tags(self):
        r = []
        for t in self.post.all():
            r.append([t.mbp_t_tid.mbt_id, t.mbp_t_tid.mbt_name, t.mbp_t_tid.mbt_colormark])
        return r

    def month_list():
        # month_map = ['January', 'February', 'March', 'April', 'May', 'June',
        #             'July', 'August', 'September', 'October', 'November', 'December']
        
        month_map = ['一月', '二月', '三月', '四月', '五月', '六月',
                     '七月', '八月', '九月', '十月', '十一月', '十二月']
                     
        post = Post.objects.all()
        year_month = set()
        for p in post:
            year_month.add((p.mbp_created_at.year, p.mbp_created_at.month))

        counter = {}.fromkeys(year_month, 0)
        for p in post:
            counter[(p.mbp_created_at.year, p.mbp_created_at.month)] += 1

        year_month_number_c = []
        # year_month_number = []
        for key in counter:
            year_month_number_c.append(
                [key[0], key[1], month_map[key[1]-1], counter[key]])

        year_month_number_c.sort(reverse=True)

        if len(year_month_number_c) > 24:
            year_month_number = year_month_number_c[:23]
            temp = year_month_number_c[24:]
            for t in temp:
                post_ttl += t[3]
            year_month_number.append(['Before above', 0, '', post_ttl])
        else:
            year_month_number = year_month_number_c.copy()

        return {'year_month_number': year_month_number}

    class Meta:
        db_table = 'mb_post'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-mbp_created_at']


# Table: MB_COMMENT
class Comment(models.Model):
    mbc_id = models.CharField('Comment ID', max_length=8, primary_key=True)
    # mbc_auther_id = models.IntegerField('Auther ID')
    mbc_auther_id = models.ForeignKey(
        MyUser, to_field='id', on_delete=models.CASCADE, db_column='mbc_auther_id', verbose_name='Auther ID')
    mbc_auther = models.CharField('Auther Name', max_length=20)
    mbc_content = models.TextField('Comment Content')
    mbc_created_at = models.DateTimeField('Create DateTime', auto_now_add=True)
    mbc_last_at = models.DateTimeField('Last Modify DateTime', auto_now=True)
    # mbc_post_id = models.CharField('Post ID', max_length=8)
    mbc_post_id = models.ForeignKey(
        Post, to_field='mbp_id', on_delete=models.CASCADE, db_column='mbc_post_id', verbose_name='Post ID')
    # mbc_reply_id = models.CharField('Replied Comment ID', max_length=8, default='0000')
    mbc_reply_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True,
                                     blank=True, db_column='mbc_reply_id', verbose_name='Comment ID')
    mbc_publish_opt = models.BooleanField('Publish Option', default=True)
    mbc_upvotes = models.IntegerField('Up voted times', default=0)
    mbc_downvotes = models.IntegerField('Down voted times', default=0)

    def __str__(self):
        return str(self.mbc_id)

    @property
    def has_child_reply(self):
        n = Comment.objects.filter(mbc_post_id=self.mbc_post_id, mbc_reply_id=self.mbc_id).count()
        return True if n > 1 else False

    def get_all_child_reply(self, include_self=False):
        r = []
        if include_self:
            r.append(self)

        for c in Comment.objects.filter(mbc_post_id=self.mbc_post_id, mbc_reply_id=self.mbc_id).exclude(mbc_reply_id=F('mbc_id')):
            _r = c.get_all_child_reply(include_self=True)
            if 0 < len(_r):
                r.extend(_r)
        return r

    class Meta:
        db_table = 'mb_comment'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comment'
        ordering = ['-mbc_created_at']


# Table: MB_POST_STATIC
class Post_Static(models.Model):
    # mbp_s_pid = models.CharField(max_length=8, primary_key=True)
    mbp_s_pid = models.OneToOneField(Post, to_field='mbp_id', on_delete=models.CASCADE,
                                     primary_key=True, db_column='mbp_s_pid', related_name='post_static', verbose_name='Post ID')
    mbp_s_reads = models.IntegerField('Read times', default=0)
    mbp_s_comments = models.IntegerField('Commment times', default=0)
    mbp_s_upvotes = models.IntegerField('Up vote times', default=0)
    mbp_s_downvotes = models.IntegerField('Down vote times', default=0)

    def __str__(self):
        return str(self.mbp_s_pid)

    class Meta:
        db_table = 'mb_post_static'
        verbose_name = 'Post_Statics'
        verbose_name_plural = 'Post_Statics'
        ordering = ['mbp_s_pid']


# Table: MB_TAG
class Tag(models.Model):
    mbt_id = models.IntegerField(primary_key=True)
    mbt_name = models.CharField(max_length=20)
    mbt_count = models.IntegerField(default=0)
    mbt_colormark = models.CharField(max_length=20)
    mbt_status = models.BooleanField(default=True)

    def __str__(self):
        return self.mbt_name

    def get_absolute_url(self):
        return reverse('tag', args=[self.mbt_id])

    class Meta:
        db_table = 'mb_tag'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


# Table: MB_POST_TAG
class Post_Tag(models.Model):
    id = models.AutoField(primary_key=True, default=0)
    mbp_t_pid = models.ForeignKey(Post, to_field='mbp_id', on_delete=models.CASCADE,
                                  db_column='mbp_t_pid', related_name='post', verbose_name='Post ID')
    mbp_t_tid = models.ForeignKey(Tag, to_field='mbt_id', on_delete=models.CASCADE,
                                  db_column='mbp_t_tid', related_name='tag', verbose_name='Tag ID')
    mbp_t_created_at = models.DateTimeField(
        'Link Create DateTime', auto_now_add=True)

    class Meta:
        db_table = 'mb_post_tag'
        unique_together = ("mbp_t_pid", "mbp_t_tid")
