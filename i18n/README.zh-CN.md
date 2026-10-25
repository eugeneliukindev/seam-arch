<p align="center">
  <img src="../assets/hero.png" width="880" alt="seam-arch：六种语言中通过 31/35 项设计检查，没有它只通过 8 项；所有行为检查均通过。">
</p>

<p align="center">
  <em>代码该放哪儿由它决定，没有东西会放错地方。</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/one%20file-379%20words-111111?style=flat-square" alt="一个文件，379 个词">
  <img src="https://img.shields.io/badge/built%20on-Clean%20Architecture-111111?style=flat-square" alt="基于 Clean Architecture">
  <img src="https://img.shields.io/badge/measured-6%20languages-111111?style=flat-square" alt="在六种语言上测得">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT 许可证">
</p>

<p align="center">
  <a href="#示例">示例</a> &middot;
  <a href="#数据">数据</a> &middot;
  <a href="#安装">安装</a> &middot;
  <a href="#任务">任务</a> &middot;
  <a href="#来源">来源</a>
</p>

<p align="center">
  <sub><a href="../README.md">English</a> &middot; <a href="README.ru.md">Русский</a> &middot; <a href="README.es.md">Español</a> &middot; <a href="README.ko.md">한국어</a> &middot; <strong>简体中文</strong> &middot; <a href="README.ja.md">日本語</a></sub>
</p>

---

**seam-arch** 是一个 `AGENTS.md`，教编码 agent 架构：代码放在哪里，各部分之间如何依赖。驱动它的只有一个问题：*换一种做法，程序会做出不同的决定吗？* 如果不会，它就是细节，只能通过一个测试可替换的类型触及业务逻辑。

> [!NOTE]
> 基于 Robert C. Martin 的 *Clean Architecture*：依赖规则、SOLID、Humble Object、跨边界只传普通数据。每条规则都对应一个没有它 agent 就会失败的任务。

## 示例

基准测试的真实输出，有删减。图片是预览；展开下方的语言，查看 agent 在该语言中写出的代码。

### 1. 告警：一个服务里的 SOLID

**“用户可以选择短信代替邮件；没有手机号就用邮件。然后：推送。”** Python，三次运行：没有 AGENTS.md 0/3，有它 3/3。

<p align="center">
  <img src="../assets/case-alerts.png" width="880" alt="没有 seam-arch 时，服务按渠道分支。有 seam-arch 时，一个 Notifier 契约，每个渠道一个类、自带回退，在入口处选择。">
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

### 2. 结账：只在需要处设接缝

**“带有效期的优惠券，按国家计算增值税，通过 Stripe 扣款。以后也许接 PayPal。”** Python，三次运行：没有 AGENTS.md 0/3，有它 3/3。这是最难的任务：在其他语言中，五次里仍有四次 agent 给 Stripe 加了包装。

<p align="center">
  <img src="../assets/case-checkout.png" width="880" alt="没有 seam-arch 时，多了一个没人需要的 PaymentGateway 包装，时钟在内部读取。有 seam-arch 时，时间从外部传入，增值税是一张表，直接使用 Stripe 自己的类。">
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

时间参与决策，所以从外部传入。增值税是数据，所以保持为一张表。Stripe 的类本身就能伪造，所以不加包装。

### 3. 密码：契约背后的细节

**“账户需要密码。用 scrypt 加随机盐做哈希。”** 没有 AGENTS.md 0/6 种语言，有它 6/6。

<p align="center">
  <img src="../assets/case-password.png" width="880" alt="没有 seam-arch 时，服务导入 hashlib，自己运行 scrypt。有 seam-arch 时，一个 PasswordHasher 契约，服务调用它，入口处选择 ScryptHasher。">
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

服务决定谁能登录；字节如何哈希是细节，即使任务点名了它、标准库也提供了它。

## 数据

同一个 agent，分别在有无 AGENTS.md 的情况下运行。

| 语言 | 设计任务 | 没有 AGENTS.md | 有 AGENTS.md |
|---|:-:|:-:|:-:|
| Python | 10 | 2/10 | **10/10** |
| TypeScript | 5 | 1/5 | **4/5** |
| Go | 5 | 1/5 | **4/5** |
| Java | 5 | 2/5 | **4/5** |
| C# | 5 | 1/5 | **5/5** |
| Rust | 5 | 1/5 | **4/5** |

每种语言都有同样的十个任务；Python 以外目前只测了其中五个。`speculative-abstraction` 是反向制衡：规则一旦过度设计，它就会失败。两组的行为检查全部通过：seam-arch 改变的是代码放在哪里，而不是代码能否运行。

## 安装

`AGENTS.md` 是唯一的文件。保留一份副本，链接到各个 agent 读取规则的位置：

```bash
curl -fsSL --create-dirs -o ~/seam-arch/AGENTS.md https://raw.githubusercontent.com/eugeneliukindev/seam-arch/main/AGENTS.md

mkdir -p ~/.claude/rules && ln -s ~/seam-arch/AGENTS.md ~/.claude/rules/seam-arch.md   # Claude Code
ln -s ~/seam-arch/AGENTS.md ~/.codex/AGENTS.md                                       # Codex
ln -s ~/seam-arch/AGENTS.md ~/.gemini/GEMINI.md                                      # Gemini CLI
ln -s ~/seam-arch/AGENTS.md ~/.config/opencode/AGENTS.md                             # opencode
ln -s ~/seam-arch/AGENTS.md ./AGENTS.md          # one project: Cursor, Copilot, Zed and any agent that reads AGENTS.md
```

再执行一次同样的 `curl`，所有 agent 同时更新。

## 任务

每个任务都是小仓库里的一张普通工单；一个 agent 永远看不到的隐藏检查负责审视设计。数字表示通过的语言数；✗ 和 ✓ 是 Python 的结果，其他语言尚未测量。

| 任务 | 交给 agent 的要求 | 隐藏检查关注什么 | 没有 AGENTS.md | 有 AGENTS.md |
|---|---|---|:-:|:-:|
| `heavy-decision` | 总结简历：读取文件，打分 | DIP：文件读取器以参数形式传入 | 0/6 | 6/6 |
| `notify-channel` | 用户可以选择短信代替邮件 | OCP：新渠道是新类，而不是新分支 | 1/6 | 6/6 |
| `password-login` | 添加登录，用 scrypt 哈希 | DIP：哈希藏在契约后面，不在服务里 | 0/6 | 6/6 |
| `combo-checkout` | 带有效期的优惠券，按国家计算增值税，通过 Stripe 扣款 | 只在需要处设接缝：时间来自外部，增值税是数据，Stripe 不加包装 | 1/6 | 2/6 |
| `combo-alerts` | 短信，回退到邮件；第二个会话中再加推送 | SOLID：不按渠道分支，单方法契约，每个 notifier 都遵守它 | ✗ | ✓ |
| `coupon-expiry` | 拒绝过期优惠券 | DIP：时钟来自外部 | ✗ | ✓ |
| `humble-cli` | 给 CLI 加上 --overdue | Humble Object：CLI 只负责解析和打印 | ✗ | ✓ |
| `plain-records` | 根据天气预报 API 建议是否带伞 | 边界：原始载荷在边缘处转换为记录 | ✗ | ✓ |
| `second-channel` | 短信，然后在第二个会话中再加推送 | 两次修改后的 OCP | ✗ | ✓ |
| `speculative-abstraction` | 通过 Stripe 扣款，“以后也许接 PayPal” | 反向制衡：只有一个客户端就不加接口 | 6/6 | 6/6 |

## 来源

- Robert C. Martin, [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) 和 *Clean Architecture*：依赖规则、SOLID、Humble Object、边界。
- Michael Feathers, *Working Effectively with Legacy Code*：接缝。
- Miško Hevery, [Guide: Writing Testable Code](https://github.com/mhevery/guide-to-testable-code)：索要协作者，绝不自己去取。
- Robert C. Martin, *Clean Code*：标志参数、包装第三方 API。
- [Google 风格指南](https://google.github.io/styleguide/cppguide.html#Parting_Words)：遵循你周围的代码。
- Alexis King, [Parse, don't validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/)：在边界处校验。

## 许可证

[MIT](../LICENSE)。
