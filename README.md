# PaymentAPI Stripe (Django + Stripe Checkout)

Онлайн демо: https://paymentapi-pha1.onrender.com/

Проект демонстрирует оплату через Stripe Checkout:
- Оплата одного товара по `Item`.
- Оплата заказа (`Order`), который содержит несколько товаров (`OrderItem`).

> На Render Free сервис может “засыпать” после простоя; первый запрос после простоя может быть медленным.

## Админка

Данные создаются через Django admin:
- Admin: https://paymentapi-pha1.onrender.com/admin/
- Login: `admin`
- Password: `notapassword`

Через админку можно создать/отредактировать:
- `Items`
- `Orders` + `OrderItems`
- `Discounts` (Stripe coupons)
- `Taxes` (Stripe tax rates)

## API / эндпоинты

### Товар
- `GET /item/{id}` — получить информацию о товаре.
- `GET /buy/{id}` — создать Stripe Checkout Session для оплаты товара, возвращает `session.id`.

Пример:
```bash
curl -i https://paymentapi-pha1.onrender.com/item/1/
curl -i https://paymentapi-pha1.onrender.com/buy/1/
```

### Заказ

    GET /order/{pk}/ — страница заказа (позиции и итог).

    GET /order/{pk}/buy/ — создать Stripe Checkout Session для оплаты заказа, возвращает session.id.

#### Пример:

```bash
curl -i https://paymentapi-pha1.onrender.com/order/1/
curl -i https://paymentapi-pha1.onrender.com/order/1/buy/
```
### Как протестировать (пошагово)

    Зайти в админку: https://paymentapi-pha1.onrender.com/admin/

    Создать Item (цена задаётся в минимальных единицах валюты, например центы для USD).

    Создать Order и добавить OrderItem (связать с созданными Item).

    Открыть страницу заказа: https://paymentapi-pha1.onrender.com/order/<pk>/

    Нажать “Оплатить” → откроется Stripe Checkout.

## Stripe (test mode)

Оплата выполняется в Stripe test mode.

Для успешной тестовой оплаты в Stripe Checkout можно использовать тестовую карту:

    4242 4242 4242 4242

    Любая будущая дата, CVC любой.

## Важно про Stripe IDs (coupon / tax rate)

 - `stripe_coupon_id = UAarRL5G`
 - `stripe_tax_rate_id = txr_1SoN9c0tjgAS5veOwkhkHVtd`

## (Опционально) Локальный запуск (Docker) + `.env`

Проект использует конфигурацию через переменные окружения (env vars), а для локальной разработки удобно хранить их в файле `.env`. [web:809][web:810]

### 1) Создать `.env`
В корне проекта (рядом с `docker-compose.yml`) создай файл `.env`:

```env
# Django
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000

# Stripe (test mode)
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# (Опционально) URL сайта — нужен для формирования success/cancel URL
SITE_URL=http://127.0.0.1:8000
```
## Docker compose

```bash
docker compose up --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```
