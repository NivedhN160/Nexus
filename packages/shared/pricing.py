class PricingHelpers:
    @staticmethod
    def usd_to_microcents(dollars: float) -> int:
        """Convert USD dollars to micro-cents (integer)."""
        # 1 dollar = 100 cents = 100,000,000 micro-cents
        return int(dollars * 100_000_000)
        
    @staticmethod
    def microcents_to_usd(microcents: int) -> float:
        """Convert micro-cents (integer) to USD dollars."""
        return microcents / 100_000_000.0

    @staticmethod
    def calculate_token_cost(input_tokens: int, output_tokens: int, input_price_per_1m: float, output_price_per_1m: float) -> int:
        """Calculate LLM cost in micro-cents."""
        input_cost = (input_tokens / 1_000_000) * input_price_per_1m
        output_cost = (output_tokens / 1_000_000) * output_price_per_1m
        return PricingHelpers.usd_to_microcents(input_cost + output_cost)
