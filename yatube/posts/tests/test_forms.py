import tempfile

from django.conf import settings
from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='StasBasov')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )

        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
            group=cls.group,
        )

    def setUp(self):
        cache.clear()

    def test_post_create(self):
        """При создании нового поста создаётся новая запись в базе данных """

        posts_count_before = Post.objects.count()

        Post.objects.create(
            text='Новый тестовый пост',
            author=self.user,
            group=self.group,
        )
        posts_count_after = Post.objects.count()
        self.assertEqual(posts_count_before + 1, posts_count_after)

    def test_post_edit(self):
        """При редактировании происходит изменение поста в базе данных"""

        post_edited_content = {
            'text': 'Новый текст',
            'group': self.group.id
        }
        response = self.authorized_client.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}
            ),
            data=post_edited_content
        )
        edited_text = self.post.text
        self.assertRedirects(response, reverse(
            'posts:post_detail',
            kwargs={'post_id': self.post.id}))
        self.assertEqual(self.post.text, edited_text)

    def test_anonym_cant_create_post(self):
        """Анонимный пользователь не может создать пост"""

        posts_count_before = Post.objects.count()

        new_post_content = {
            'text': 'Новый текст',
            'group': self.group,
        }

        self.client.post(reverse(
            'posts:post_create'),
            data=new_post_content,)

        posts_count_after = Post.objects.count()
        self.assertEqual(posts_count_before, posts_count_after)
