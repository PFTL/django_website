from wagtail.core.blocks import StaticBlock


class NewsletterSubscribe(StaticBlock):
    class Meta:
        admin_text = 'Add a newsletter subscription box in between the text'
        template = 'blog/newsletter_inline.html'
        icon = 'email'


class BookInline(StaticBlock):
    class Meta:
        admin_text = 'Add a link to the book page'
        template = 'blog/book_inline.html'
        icon = 'book'