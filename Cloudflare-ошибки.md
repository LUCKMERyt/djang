# Справочник ошибок Cloudflare

Ошибки Cloudflare не всегда доходят до Django. Сначала сохраните полный текст
ошибки, URL, дату/время с часовым поясом и Ray ID; затем сопоставьте их с
Cloudflare Security Events и логами origin, прокси и firewall. Не публикуйте
пароли, токены Tunnel, приватные ключи или конфигурации с секретами.

| Код | Кратко | Инструкция |
| --- | --- | --- |
| 520 | Origin вернул пустой или неожиданный ответ | [520.md](./520.md) |
| 521 | Origin отклонил соединение или недоступен | [521.md](./521.md) |
| 522 | Не удалось подключиться к origin вовремя | [522.md](./522.md) |
| 523 | Нет маршрута к origin | [523.md](./523.md) |
| 524 | Origin принял соединение, но долго не отвечает | [524.md](./524.md) |
| 525 | Не прошёл TLS handshake с origin | [525.md](./525.md) |
| 526 | Сертификат origin не прошёл проверку | [526.md](./526.md) |
| 530 | Общая ошибка; важны подкод и текст страницы | [530.md](./530.md) |
| 1016 | Не разрешается DNS-имя origin | [1016.md](./1016.md) |
| 1020 | Запрос заблокирован правилом безопасности | [1020.md](./1020.md) |
| 1033 | Cloudflare Tunnel не видит активный connector | [Ошибка 1033.md](./Ошибка%201033.md) |

## Официальные справочники

- [Cloudflare 5xx errors](https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-5xx-errors/)
- [Cloudflare 1xxx errors](https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-1xxx-errors/)
- [Ошибки Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/troubleshoot-tunnels/common-errors/)

`runserver` на `127.0.0.1` обслуживает только локальную разработку и не может
быть production-origin для Cloudflare.
