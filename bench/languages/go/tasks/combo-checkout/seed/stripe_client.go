package shop

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"strconv"
	"strings"
)

// StripeClient talks to Stripe's charges API; production sets BaseURL to https://api.stripe.com.
type StripeClient struct {
	BaseURL string
	APIKey  string
	HTTP    *http.Client
}

// CreateCharge charges source and returns the charge id.
func (c *StripeClient) CreateCharge(ctx context.Context, amountCents int64, currency, source string) (string, error) {
	form := url.Values{
		"amount":   {strconv.FormatInt(amountCents, 10)},
		"currency": {strings.ToLower(currency)},
		"source":   {source},
	}
	request, err := http.NewRequestWithContext(ctx, http.MethodPost, c.BaseURL+"/v1/charges", strings.NewReader(form.Encode()))
	if err != nil {
		return "", fmt.Errorf("stripe: %w", err)
	}
	request.SetBasicAuth(c.APIKey, "")
	request.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	response, err := c.HTTP.Do(request)
	if err != nil {
		return "", fmt.Errorf("stripe: %w", err)
	}
	defer response.Body.Close()
	if response.StatusCode != http.StatusOK {
		return "", fmt.Errorf("stripe: charge refused: %s", response.Status)
	}
	var charge struct {
		ID string `json:"id"`
	}
	if err := json.NewDecoder(response.Body).Decode(&charge); err != nil {
		return "", fmt.Errorf("stripe: %w", err)
	}
	return charge.ID, nil
}
