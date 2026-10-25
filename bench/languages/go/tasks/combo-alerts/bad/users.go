package alerts

// Channel is how a user chose to get alerts.
type Channel string

// The channels a user can choose; a user who never chose has the zero Channel and gets mail.
const (
	ChannelEmail Channel = "email"
	ChannelSMS   Channel = "sms"
	ChannelPush  Channel = "push"
)

// User is someone who receives alerts, by the channel they chose.
type User struct {
	ID          int
	Email       string
	Phone       string // empty when the user gave none
	DeviceToken string // empty when the user has not installed the app
	Channel     Channel
}
