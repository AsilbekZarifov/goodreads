from django.test import TestCase
from django.urls import reverse
from books.models import Book
from users.models import CustomUser


# Create your tests here.


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"))

        self.assertContains(response, "No books found.")

    def test_books_list(self):
        book1 = Book.objects.create(title="Book1", description="Description1", isbn="1111")
        book2 = Book.objects.create(title="Book2", description="Description2", isbn="2222")
        book3 = Book.objects.create(title="Book3", description="Description3", isbn="3333")

        response = self.client.get(reverse('books:list') + "?page_size=2")

        for book in [book1, book2]:
            self.assertContains(response, book.title)

        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?page=2&page_size=2")

        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="1111")
        response = self.client.get(reverse("books:detail", kwargs={"id": book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search_books(self):
        book1 = Book.objects.create(title="sport", description="Description1", isbn="1111")
        book2 = Book.objects.create(title="game", description="Description2", isbn="2222")
        book3 = Book.objects.create(title="book", description="Description3", isbn="3333")

        response = self.client.get(reverse("books:list")+"?q=book")
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)

        response = self.client.get(reverse("books:list") + "?q=sport")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=game")
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)


class BookReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title="sport", description="Description1", isbn="1111")

        user = CustomUser.objects.create(
            username="asilbek", first_name="asilbek", last_name="Zarifov", email="asilbek@gmail.com"
        )
        user.set_password("somepass")
        user.save()
        self.client.login(username="hamidbek2669", password="somepass")
        response = self.client.post(reverse("books:reviews", kwargs={"id": book.id}), data={
            "stars_given" :3,
            "comment": "Nice book"
        })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, "Nice book")
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)