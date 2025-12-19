import pytest
from main import BooksCollector


class TestBooksCollector:

    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    def test_add_new_book_already_added_book(self, collector):
        collector.add_new_book("Гарри Поттер")
        collector.add_new_book("Гарри Поттер")
        assert len(collector.get_books_genre()) == 1

    def test_add_new_book_name_out_of_range_short(self, collector):
        collector.add_new_book("")
        assert len(collector.get_books_genre()) == 0

    @pytest.mark.parametrize("name, expected_count", [
        ("", 0),
        ("A" * 41, 0),
        ("A", 1),
        ("A" * 40, 1),
        ("  ", 1),
        ])
    def test_add_new_book_various_names(self, collector, name, expected_count):
        collector.add_new_book(name)
        assert len(collector.get_books_genre()) == expected_count

    def test_set_book_genre_to_existing_book(self, collector):
        collector.add_new_book("Гарри Поттер")
        collector.set_book_genre("Гарри Поттер", "Фантастика")
        assert collector.get_book_genre("Гарри Поттер") == "Фантастика"


    def test_set_book_genre_to_not_existing_book(self, collector):
        collector.set_book_genre("Несуществующая книга", "Фантастика")
        assert collector.get_book_genre("Несуществующая книга") is None

    @pytest.mark.parametrize("genre", [
        "Фантастика",
        "Ужасы",
        "Детективы",
        "Мультфильмы",
        "Комедии",
        ])
    def test_set_book_genre_valid_genres(self, collector, genre):
        collector.add_new_book("Гарри Поттер")
        collector.set_book_genre("Гарри Поттер", genre)
        assert collector.get_book_genre("Гарри Поттер") == genre

    @pytest.mark.parametrize("genre", [
        "Роман",
        "Драма",
        "",
        None,
        ])
    def test_set_book_genre_invalid_genres(self, collector, genre):
        collector.add_new_book("Гарри Поттер")
        collector.set_book_genre("Гарри Поттер", genre)
        assert collector.get_book_genre("Гарри Поттер") == ""

    def test_get_books_with_specific_genre_by_genre(self, collector):
        collector.add_new_book("Гарри Поттер")
        collector.set_book_genre("Гарри Поттер", "Фантастика")
        collector.add_new_book("Ночной дозор")
        collector.set_book_genre("Ночной дозор", "Фантастика")
        books = collector.get_books_with_specific_genre("Фантастика")
        assert len(books) == 2

    def test_get_books_for_children(self, collector):
        collector.add_new_book("Шрек")
        collector.set_book_genre("Шрек", "Мультфильмы")
        collector.add_new_book("Гарри Поттер")
        collector.set_book_genre("Гарри Поттер", "Фантастика")
        collector.add_new_book("Ночной дозор")
        collector.set_book_genre("Ночной дозор", "Ужасы")
        children_books = collector.get_books_for_children()
        assert len(children_books) == 2
        
    def test_add_book_in_favorites_added_in_favorites_book(self, collector):
        collector.add_new_book("Гарри Поттер")
        collector.add_book_in_favorites("Гарри Поттер")
        collector.add_book_in_favorites("Гарри Поттер")
        assert len(collector.get_list_of_favorites_books()) == 1

    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book("Гарри Поттер")
        collector.add_book_in_favorites("Гарри Поттер")
        collector.delete_book_from_favorites("Гарри Поттер")
        assert len(collector.get_list_of_favorites_books()) == 0

    def test_get_list_of_favorites_books(self, collector):
        collector.add_new_book("Гарри Поттер")
        collector.add_new_book("Шрек")
        collector.add_book_in_favorites("Гарри Поттер")
        collector.add_book_in_favorites("Шрек")
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 2
        
    def test_new_book_has_no_genre_by_default(self, collector):
        collector.add_new_book("Гарри Поттер")
        assert collector.get_book_genre("Гарри Поттер") == ""

    def test_books_with_adult_genre_not_in_children_list(self, collector):
        collector.add_new_book("Ночной дозор")
        collector.set_book_genre("Ночной дозор", "Ужасы")
        children_books = collector.get_books_for_children()
        assert "Ночной дозор" not in children_books

    def test_books_with_child_genre_in_children_list(self, collector):
        collector.add_new_book("Дом странных детей")
        collector.set_book_genre("Дом странных детей", "Фантастика")
        children_books = collector.get_books_for_children()
        assert "Дом странных детей" in children_books