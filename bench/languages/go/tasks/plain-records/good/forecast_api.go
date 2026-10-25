package weather

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
)

// ForecastAPI talks to the forecast provider; production sets BaseURL to https://forecast.example.com.
type ForecastAPI struct {
	BaseURL string
	HTTP    *http.Client
}

// Fetch returns the provider's raw JSON for city, today first.
//
// For example {"daily": [{"pop": 0.7, "tmax": 12.3}, {"pop": 0.1, "tmax": 15.0}]},
// where pop is the probability of precipitation from 0 to 1 and tmax the
// day's highest temperature in degrees Celsius.
func (a *ForecastAPI) Fetch(ctx context.Context, city string) (map[string]any, error) {
	address := a.BaseURL + "/v1/forecast?" + url.Values{"city": {city}}.Encode()
	request, err := http.NewRequestWithContext(ctx, http.MethodGet, address, nil)
	if err != nil {
		return nil, fmt.Errorf("forecast: %w", err)
	}
	response, err := a.HTTP.Do(request)
	if err != nil {
		return nil, fmt.Errorf("forecast: %w", err)
	}
	defer response.Body.Close()
	if response.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("forecast: %s", response.Status)
	}
	var payload map[string]any
	if err := json.NewDecoder(response.Body).Decode(&payload); err != nil {
		return nil, fmt.Errorf("forecast: %w", err)
	}
	return payload, nil
}

// Today returns today's forecast for city.
func (a *ForecastAPI) Today(ctx context.Context, city string) (Forecast, error) {
	payload, err := a.Fetch(ctx, city)
	if err != nil {
		return Forecast{}, err
	}
	days, _ := payload["daily"].([]any)
	if len(days) == 0 {
		return Forecast{}, fmt.Errorf("forecast: no days for %s", city)
	}
	today, _ := days[0].(map[string]any)
	chance, ok := today["pop"].(float64)
	if !ok {
		return Forecast{}, fmt.Errorf("forecast: no chance of rain for %s", city)
	}
	return Forecast{RainChance: chance}, nil
}
