from PIL import Image
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.crypto import get_random_string
import string
from django.db.models import CharField, Model, SlugField
# from autoslug import AutoSlugField
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, phone=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=30, default='new user')
    address = models.TextField(null=True)
    profile_pic = models.ImageField(blank=True, null=True)
    DOB = models.DateField(blank=True, null=True)
    slug = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=12, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def get_cart_total(self):
        cartdetails = self.cartdetail_set.all()
        total = sum([item.get_total for item in cartdetails])
        return total

    @property
    def get_cart_items(self):
        cartdetails = self.cartdetail_set.all()
        total = sum([item.quantity for item in cartdetails])
        return total


class Shop(models.Model):
    objects = True
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=300, null=True)
    slug = SlugField(default='', editable=True, max_length=100)
    profile_pic = models.ImageField(blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    address = models.CharField(max_length=1000, null=True)
    phone = models.CharField(max_length=12, null=True)
    active = models.BooleanField(default=True, null=False, blank=False)
    pickup = models.BooleanField(default=False, null=False, blank=False)
    delivery = models.BooleanField(default=False, null=False, blank=False)
    #created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True, null=True)

    # @property
    # def products(self):
    #     return
    def __str__(self):
        return self.slug

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name, allow_unicode=False).replace(' ', '-')
    #     super(Shop, self).save(*args, *kwargs)
    #     return True


class Cart(models.Model):
    user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    slug = SlugField(default='', editable=False, max_length=100)
    # cart_details = models.JSONField(null=True)
    #cart_no = models.CharField(max_length=30)


    def save(self, *args, **kwargs):
        self.cart_no = get_random_string(8, allowed_chars=string.ascii_uppercase + string.digits)
        self.slug = slugify(self.cart_no, allow_unicode=False)
        super(Cart, self).save(*args, **kwargs)
        return True






class Category(models.Model):
    objects = True
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=300, null=True)
    slug = SlugField(default='', editable=True, max_length=100)

    def __str__(self):
        return self.slug



    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name, allow_unicode=False).replace(' ', '-')
    #     super(Category, self).save(*args, **kwargs)
    #     return True


class Product(models.Model):
    objects = True
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=300, null=True)
    slug = SlugField(default='', editable=True, max_length=100)
    selling_price = models.DecimalField(max_digits=10, decimal_places=5)
    actual_price = models.DecimalField(max_digits=10, decimal_places=5)
    unit = models.CharField(max_length=20, null=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.slug

    @property
    def imageURL(self):
        #return 'static/images/'+self.id+'.jpg'
        try:
            url='static/images/'+str(self.id)+'.jpg'
            return url
        except:
            return 'static/images/placeholder.png'




class Order(models.Model):
    objects = True
    name = models.CharField(max_length=100, null=True)
    slug = SlugField(default='', editable=True, max_length=100,null=True)
    phone = models.CharField(max_length=12, null=True)
    order_no = models.CharField(max_length=30, editable=False)
    status = models.CharField(max_length=100, null=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.slug

    # @property
    # def get_cart_items(self):
    #     cartdetail = self.cartdetail_set.all()
    #     total = sum([item.get_total for item in cartdetail])
    #     return total
    #
    # @property
    # def get_cart_items(self):
    #     cartdetail = self.cartdetail_set.all()
    #     total = sum([item.quantity for item in cartdetail])
    #     return total

    # def save(self, *args, **kwargs):
    #      self.order_no = get_random_string(8, allowed_chars=string.ascii_uppercase + string.digits)
    #      self.slug = slugify(self.order_no, allow_unicode=False)
    #      super(Order, self).save(*args, **kwargs)
    #      return True


class CartDetail(models.Model):
    objects = True
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(null=False, default=0)

    def save(self, *args, **kwargs):
        super(CartDetail, self).save(*args, **kwargs)
        return True

    @property
    def get_total(self):
        total = (self.product_id.selling_price * self.quantity)
        return total


class OrderDetail(models.Model):
    objects= True
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(null=False, default=1)

    def products(self):
        return Product.objects.filter(id=self.product_id).values_list('name', flat=True)

    # @property
    # def get_total(self):
    #     total = self.product_id.selling_price * self.quantity
    #     return total
    # def save(self, *args, **kwargs):
    #     super(OrderDetail, self).save(*args, **kwargs)
    #     return True
