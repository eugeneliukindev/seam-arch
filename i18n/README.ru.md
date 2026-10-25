<p align="center">
  <img src="../assets/hero.png" width="880" alt="seam-arch: 31 из 35 проверок дизайна против 8 без него, на шести языках; все проверки поведения проходят.">
</p>

<p align="center">
  <em>Он решает, где лежит код, и ничего не оказывается не на своём месте.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/one%20file-379%20words-111111?style=flat-square" alt="Один файл, 379 слов">
  <img src="https://img.shields.io/badge/built%20on-Clean%20Architecture-111111?style=flat-square" alt="Построено на Clean Architecture">
  <img src="https://img.shields.io/badge/measured-6%20languages-111111?style=flat-square" alt="Измерено на шести языках">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="Лицензия MIT">
</p>

<p align="center">
  <a href="#примеры">Примеры</a> &middot;
  <a href="#цифры">Цифры</a> &middot;
  <a href="#установка">Установка</a> &middot;
  <a href="#задачи">Задачи</a> &middot;
  <a href="#источники">Источники</a>
</p>

<p align="center">
  <sub><a href="../README.md">English</a> &middot; <strong>Русский</strong> &middot; <a href="README.es.md">Español</a> &middot; <a href="README.ko.md">한국어</a> &middot; <a href="README.zh-CN.md">简体中文</a> &middot; <a href="README.ja.md">日本語</a></sub>
</p>

---

**seam-arch** — это один `AGENTS.md`, который учит агента-программиста архитектуре: где лежит код и как его части зависят друг от друга. В основе один вопрос: *если сделать это иначе, решит ли программа что-нибудь по-другому?* Если нет, это деталь, и до бизнес-логики она доходит только через тип, который тест может подменить.

> [!NOTE]
> Построено на *Clean Architecture* Роберта Мартина: Dependency Rule, SOLID, Humble Object, простые данные через границы. Каждое правило заслужило свою строку на задаче, которую агенты без него проваливают.

## Примеры

Реальный вывод бенчмарка, с сокращениями. Картинка — это превью; раскройте язык под ней, чтобы увидеть код, который там написал агент.

### 1. Оповещения: SOLID в одном сервисе

**«Пользователи могут выбрать SMS вместо email; нет телефона — значит email. Потом: push».** Python, три прогона: без AGENTS.md 0/3, с ним 3/3.

<p align="center">
  <img src="../assets/case-alerts.png" width="880" alt="Без seam-arch сервис ветвится по каналу. С seam-arch один контракт Notifier, у каждого канала свой класс со своим запасным вариантом, выбор в точке входа.">
</p>

<details>
<summary><strong>Python</strong></summary>

```python
class Notifier(Protocol):
    def notify(self, user: User, text: str) -> None: ...

class AlertService:
    def __init__(self, notifiers: Mapping[Channel, Notifier]) -> None:
        self._notifiers = notifiers
    def alert(self, user, text):
        self._notifiers[user.channel].notify(user, text)

# app.py
return AlertService({"email": EmailNotifier(smtp), "sms": SmsNotifier(sms)})
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```ts
export interface Notifier {
  notify(user: User, text: string): void;
}

export class AlertService {
  constructor(private readonly notifiers: Readonly<Record<Channel, Notifier>>) {}
  alert(user: User, text: string): void {
    this.notifiers[user.channel].notify(user, text);
  }
}

// app.ts
return new AlertService({ email: new EmailNotifier(smtp), sms: new SmsNotifier(sms) });
```
</details>

<details>
<summary><strong>Go</strong></summary>

```go
type Notifier interface {
	Notify(user User, text string) error
}

func (s *AlertService) Alert(user User, text string) error {
	n, ok := s.notifiers[user.Channel]
	if !ok {
		return fmt.Errorf("%w: %q", ErrUnknownChannel, user.Channel)
	}
	return n.Notify(user, text)
}

// app.go
return NewAlertService(map[string]Notifier{"email": email, "sms": NewSmsNotifier(sms)})
```
</details>

<details>
<summary><strong>Java</strong></summary>

```java
public interface Notifier {
    void deliver(User user, String text);
}

public AlertService(Map<Channel, Notifier> notifiers) { this.notifiers = Map.copyOf(notifiers); }

public void alert(User user, String text) {
    notifiers.get(user.channel()).deliver(user, text);
}

// App.java
return new AlertService(Map.of(Channel.EMAIL, new EmailNotifier(smtp), Channel.SMS, new SmsNotifier(sms)));
```
</details>

<details>
<summary><strong>C#</strong></summary>

```csharp
public interface INotifier
{
    void Notify(User user, string text);
}

public sealed class AlertService(IReadOnlyDictionary<Channel, INotifier> notifiers)
{
    public void Alert(User user, string text) => notifiers[user.Channel].Notify(user, text);
}

// App.cs
new Dictionary<Channel, INotifier> { [Channel.Email] = new EmailNotifier(smtp), [Channel.Sms] = new SmsNotifier(sms) }
```
</details>

<details>
<summary><strong>Rust</strong></summary>

```rust
pub trait Notifier {
    fn notify(&self, user: &User, text: &str) -> Result<(), NotifyError>;
}

pub struct AlertService {
    notifiers: HashMap<Channel, Rc<dyn Notifier>>,
}

// app.rs
notifiers.insert(Channel::Email, Rc::new(EmailNotifier::new(smtp)));
notifiers.insert(Channel::Sms, Rc::new(SmsNotifier::new(sms)));
AlertService::new(notifiers)
```
</details>

### 2. Оформление заказа: шов только там, где он нужен

**«Купон со сроком действия, НДС по стране, оплата через Stripe. Может, потом PayPal».** Python, три прогона: без AGENTS.md 0/3, с ним 3/3. Самая трудная задача: на других языках агент всё равно оборачивает Stripe в четырёх случаях из пяти.

<p align="center">
  <img src="../assets/case-checkout.png" width="880" alt="Без seam-arch ненужная обёртка PaymentGateway и часы, которые читаются внутри. С seam-arch время приходит снаружи, НДС — таблица, используется собственный класс Stripe.">
</p>

<details>
<summary><strong>Python</strong></summary>

```python
class Checkout:
    def __init__(self, *, coupons: CouponBook, vat_rates: Mapping[str, float], client: StripeClient) -> None:
        self._coupons = coupons
        self._vat_rates = vat_rates
        self._client = client

    def pay(self, cart: Cart, code: str, country: str, card_token: str) -> str:
        coupon = self._coupons.redeem(code)          # refuses an expired coupon, on the injected clock
        discounted = cart.total * (100 - coupon.percent) / 100
        total = discounted * (1 + self._vat_rates.get(country, 0.0))
        return self._client.create_charge(amount_cents=round(total * 100), currency="eur", source=card_token)

# app.py
VAT_RATES = {"GB": 0.20, "DE": 0.19, "NL": 0.21}

def build_checkout(client: StripeClient) -> Checkout:
    coupons = CouponBook(now=lambda: datetime.now(UTC))
    return Checkout(coupons=coupons, vat_rates=VAT_RATES, client=client)
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```ts
export function amountDue(totalCents: number, couponPercent: number, country: string): number {
  const discounted = Math.round((totalCents * (100 - couponPercent)) / 100);
  return discounted + Math.round((discounted * (VAT_PERCENT[country] ?? 0)) / 100);
}

export class Checkout {
  constructor(
    private readonly coupons: CouponBook,
    private readonly client: StripeClient,
    private readonly now: () => Date,
  ) {}
  async pay(cart: Cart, code: string, country: string, cardToken: string): Promise<string> {
    const coupon = redeem(this.coupons, code, this.now());
    const amountCents = amountDue(Math.round(cart.total * 100), coupon.percent, country);
    return this.client.createCharge({ amountCents, currency: "EUR", source: cardToken });
  }
}

// app.ts
return new Checkout(new CouponBook(), client, () => new Date());
```
</details>

<details>
<summary><strong>Go</strong></summary>

```go
type Checkout struct {
	Coupons    *CouponBook
	Charger    Charger // StripeClient is one
	VATPercent map[string]int64
	Now        func() time.Time
}

func (c *Checkout) Pay(ctx context.Context, cart Cart, code, country, cardToken string) (string, error) {
	total := cart.TotalCents
	if code != "" {
		percent, err := c.Coupons.Redeem(code, c.Now())
		if err != nil {
			return "", err
		}
		total -= total * percent / 100
	}
	total += (total*c.VATPercent[country] + 50) / 100
	return c.Charger.CreateCharge(ctx, total, "EUR", cardToken)
}

// app.go
return &Checkout{Coupons: NewCouponBook(), Charger: client,
	VATPercent: map[string]int64{"GB": 20, "DE": 19, "NL": 21}, Now: time.Now}
```
</details>

<details>
<summary><strong>Java</strong></summary>

```java
public Checkout(CouponBook coupons, VatRates vat, StripeClient client, Clock clock) { ... }

public String pay(Cart cart, String code, String country, String cardToken) {
    Coupon coupon = coupons.find(code);
    if (!clock.instant().isBefore(coupon.expires())) {
        throw new CouponExpiredException(code);
    }
    long cents = priceInCents(cart.total(), coupon.percent(), vat.rateFor(country));
    return client.createCharge(cents, "eur", cardToken);
}

// App.java
VatRates vat = new VatRates(Map.of("GB", new BigDecimal("0.20"), "DE", new BigDecimal("0.19"), "NL", new BigDecimal("0.21")));
return new Checkout(new CouponBook(), vat, client, Clock.systemUTC());
```
</details>

<details>
<summary><strong>C#</strong></summary>

```csharp
public sealed class Checkout(
    CouponBook coupons,
    IReadOnlyDictionary<string, decimal> vatRates,
    StripeClient client,
    Func<DateTimeOffset> now)
{
    public string Pay(Cart cart, string code, string country, string cardToken)
    {
        var coupon = coupons.Find(code);
        if (coupon.Expires < now()) throw new CouponExpiredException(code);
        var vat = vatRates.GetValueOrDefault(country, 0m);
        return client.CreateCharge(Cents(cart.Total, coupon.Percent, vat), "eur", cardToken);
    }
}

// App.cs
new Checkout(new CouponBook(), VatRates, client, () => DateTimeOffset.UtcNow);
```
</details>

<details>
<summary><strong>Rust</strong></summary>

```rust
pub struct Checkout {
    pub coupons: CouponBook,
    client: Box<dyn StripeClient>,
    now: Box<dyn Fn() -> SystemTime>,
}

impl Checkout {
    pub fn pay(&self, cart: &Cart, code: &str, country: &str, card_token: &str) -> Result<String, CheckoutError> {
        let coupon = self.coupons.redeem(code, (self.now)())?;
        let amount = price_cents(cart.total_cents, coupon.percent, vat_percent(country));
        Ok(self.client.create_charge(amount, "EUR", card_token))
    }
}

// vat.rs
pub fn vat_percent(country: &str) -> u64 {
    match country { "GB" => 20, "DE" => 19, "NL" => 21, _ => 0 }
}

// app.rs
Checkout::new(client, Box::new(SystemTime::now))
```
</details>

Время влияет на решение, поэтому приходит снаружи. НДС — это данные, поэтому остаётся таблицей. Класс Stripe и так можно подменить, поэтому обёртки у него нет.

### 3. Пароли: деталь за контрактом

**«Аккаунтам нужны пароли. Хешируй через scrypt со случайной солью».** Без AGENTS.md 0/6 языков, с ним 6/6.

<p align="center">
  <img src="../assets/case-password.png" width="880" alt="Без seam-arch сервис импортирует hashlib и сам запускает scrypt. С seam-arch контракт PasswordHasher, сервис вызывает его, точка входа выбирает ScryptHasher.">
</p>

<details>
<summary><strong>Python</strong></summary>

```python
class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> bytes: ...
    @abstractmethod
    def verify(self, password: str, password_hash: bytes) -> bool: ...

class AccountService:
    def __init__(self, *, users: UserStore, hasher: PasswordHasher) -> None:
        self._users = users
        self._hasher = hasher

    def log_in(self, email: str, password: str) -> bool:
        user = self._users.find(email)
        if user is None or not user.password_hash:
            return False
        return self._hasher.verify(password, user.password_hash)

# app.py
return AccountService(users=InMemoryUsers(), hasher=ScryptHasher())
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```ts
export interface PasswordHasher {
  hash(password: string): string;
  verify(password: string, hash: string): boolean;
}

export class AccountService {
  constructor(
    private readonly users: UserStore,
    private readonly hasher: PasswordHasher,
  ) {}
  logIn(email: string, password: string): boolean {
    const user = this.users.find(email);
    return user !== undefined && this.hasher.verify(password, user.passwordHash);
  }
}

// app.ts
return new AccountService(new InMemoryUsers(), new ScryptHasher());
```
</details>

<details>
<summary><strong>Go</strong></summary>

```go
type PasswordHasher interface {
	Hash(password string) ([]byte, error)
	Matches(hash []byte, password string) bool
}

func NewAccountService(users UserStore, hasher PasswordHasher) *AccountService {
	return &AccountService{users: users, hasher: hasher}
}

func (s *AccountService) LogIn(email, password string) (bool, error) {
	user, ok := s.users.Find(email)
	if !ok {
		return false, nil
	}
	return s.hasher.Matches(user.PasswordHash, password), nil
}

// app.go
return NewAccountService(NewInMemoryUsers(), PBKDF2Hasher{})
```
</details>

<details>
<summary><strong>Java</strong></summary>

```java
public interface PasswordHasher {
    byte[] hash(String password);
    boolean matches(String password, byte[] stored);
}

public AccountService(UserStore users, PasswordHasher hasher) {
    this.users = users;
    this.hasher = hasher;
}

public boolean logIn(String email, String password) {
    return users.find(email)
            .filter(user -> user.passwordHash().length > 0)
            .map(user -> hasher.matches(password, user.passwordHash()))
            .orElse(false);
}

// App.java
return new AccountService(new InMemoryUsers(), new Pbkdf2PasswordHasher());
```
</details>

<details>
<summary><strong>C#</strong></summary>

```csharp
public interface IPasswordHasher
{
    byte[] Hash(string password);
    bool Verify(string password, byte[] stored);
}

public sealed class AccountService(IUserStore users, IPasswordHasher hasher)
{
    public bool LogIn(string email, string password) =>
        users.Find(email) is { } user && hasher.Verify(password, user.PasswordHash);
}

// App.cs
public static AccountService BuildService() => new(new InMemoryUsers(), new Pbkdf2PasswordHasher());
```
</details>

<details>
<summary><strong>Rust</strong></summary>

```rust
pub trait PasswordHasher {
    fn new_salt(&self) -> Vec<u8>;
    fn derive(&self, password: &str, salt: &[u8]) -> Vec<u8>;
}

pub struct AccountService {
    users: Box<dyn UserStore>,
    hasher: Box<dyn PasswordHasher>,
}

// app.rs
AccountService::new(Box::new(InMemoryUsers::default()), Box::new(KdfHasher))
```
</details>

Сервис решает, кто входит; как хешируются байты — деталь, даже когда задача её называет, а в стандартной библиотеке она есть.

## Цифры

Один и тот же агент с AGENTS.md и без.

| язык | задачи на дизайн | без AGENTS.md | с AGENTS.md |
|---|:-:|:-:|:-:|
| Python | 10 | 2/10 | **10/10** |
| TypeScript | 5 | 1/5 | **4/5** |
| Go | 5 | 1/5 | **4/5** |
| Java | 5 | 2/5 | **4/5** |
| C# | 5 | 1/5 | **5/5** |
| Rust | 5 | 1/5 | **4/5** |

На каждом языке одни и те же десять задач; за пределами Python пока измерены пять из них. `speculative-abstraction` — противовес: она проваливается, если правила переусложняют дизайн. Все проверки поведения проходят в обоих вариантах: seam-arch меняет то, где лежит код, а не то, работает ли он.

## Установка

`AGENTS.md` — единственный файл. Держите одну копию и ставьте ссылку туда, где ваши агенты читают правила:

```bash
curl -fsSL --create-dirs -o ~/seam-arch/AGENTS.md https://raw.githubusercontent.com/eugeneliukindev/seam-arch/main/AGENTS.md

mkdir -p ~/.claude/rules && ln -s ~/seam-arch/AGENTS.md ~/.claude/rules/seam-arch.md   # Claude Code
ln -s ~/seam-arch/AGENTS.md ~/.codex/AGENTS.md                                       # Codex
ln -s ~/seam-arch/AGENTS.md ~/.gemini/GEMINI.md                                      # Gemini CLI
ln -s ~/seam-arch/AGENTS.md ~/.config/opencode/AGENTS.md                             # opencode
ln -s ~/seam-arch/AGENTS.md ./AGENTS.md          # one project: Cursor, Copilot, Zed and any agent that reads AGENTS.md
```

Тот же `curl` ещё раз обновляет всех агентов сразу.

## Задачи

Каждая задача — обычный тикет в небольшом репозитории; скрытая проверка, которую агент никогда не видит, смотрит на дизайн. Число — это сколько языков прошло; ✗ и ✓ — это Python, где другие языки пока не измерены.

| задача | что просят у агента | что ищет скрытая проверка | без AGENTS.md | с AGENTS.md |
|---|---|---|:-:|:-:|
| `heavy-decision` | кратко описать резюме: прочитать файл, оценить | DIP: чтение файла приходит параметром | 0/6 | 6/6 |
| `notify-channel` | пользователи могут выбрать SMS вместо email | OCP: новый канал — новый класс, а не ветка | 1/6 | 6/6 |
| `password-login` | добавить вход, хешировать через scrypt | DIP: хеширование за контрактом, а не в сервисе | 0/6 | 6/6 |
| `combo-checkout` | купон со сроком действия, НДС по стране, оплата через Stripe | шов только там, где нужен: время снаружи, НДС как данные, без обёртки для Stripe | 1/6 | 2/6 |
| `combo-alerts` | SMS с запасным email, потом push во второй сессии | SOLID: нет ветвления по каналу, контракт из одного метода, каждый notifier его соблюдает | ✗ | ✓ |
| `coupon-expiry` | отклонять просроченные купоны | DIP: часы приходят снаружи | ✗ | ✓ |
| `humble-cli` | добавить --overdue в CLI | Humble Object: CLI только разбирает аргументы и печатает | ✗ | ✓ |
| `plain-records` | совет про зонт по API прогноза | граница: сырой ответ превращается в запись на краю | ✗ | ✓ |
| `second-channel` | SMS, потом push во второй сессии | OCP после двух правок | ✗ | ✓ |
| `speculative-abstraction` | оплата через Stripe, «может, потом PayPal» | противовес: нет интерфейса для единственного клиента | 6/6 | 6/6 |

## Источники

- Robert C. Martin, [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) и *Clean Architecture*: Dependency Rule, SOLID, Humble Object, границы.
- Michael Feathers, *Working Effectively with Legacy Code*: швы.
- Miško Hevery, [Guide: Writing Testable Code](https://github.com/mhevery/guide-to-testable-code): просите зависимости, а не добывайте их сами.
- Robert C. Martin, *Clean Code*: аргументы-флаги, обёртки над сторонними API.
- [Руководства по стилю Google](https://google.github.io/styleguide/cppguide.html#Parting_Words): следуйте окружающему коду.
- Alexis King, [Parse, don't validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/): проверяйте на границе.

## Лицензия

[MIT](../LICENSE).
