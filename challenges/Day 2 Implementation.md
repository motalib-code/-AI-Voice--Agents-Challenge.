# Day 2 - Coffee Shop Barista Agent

## What I Built

For Day 2, I transformed the base agent into a friendly coffee shop barista. The agent can now:

✔ Take voice-based coffee orders
✔ Ask follow-up questions until the order is complete
✔ Maintain a structured order format like:

```json
{
 "drinkType": "string",
 "size": "string",
 "milk": "string",
 "extras": ["string"],
 "name": "string"
}
```

✔ Save the final order as a Json summary file
✔ Respond naturally — just like a real barista ☕✨

🧪 **Optional Challenge Attempt:**
I also experimented with a dynamic HTML-based drink visualizer, where the size and extras update visually based on the order — making the experience even more engaging.

## Features Implemented

### ✅ Primary Goal (Required)

1. **Barista Persona**: Friendly barista for "Brew Haven Coffee Shop"
   
2. **Order State Management**: Maintains complete order state with:
   ```json
   {
     "drinkType": "string",
     "size": "string", 
     "milk": "string",
     "extras": ["string"],
     "name": "string"
   }
   ```

3. **Interactive Order Taking**:
   - Agent asks clarifying questions for missing information
   - Conversational and natural dialogue
   - One question at a time approach

4. **Function Tools Implemented**:
   - `update_drink_type()` - Sets the coffee drink type
   - `update_size()` - Sets size (small/medium/large)
   - `update_milk()` - Sets milk preference
   - `add_extra()` - Adds extras like whipped cream, syrups, extra shots
   - `update_name()` - Sets customer name
   - `save_order()` - Finalizes and saves order to JSON file

5. **Order Persistence**:
   - Orders saved to `backend/orders/` directory
   - Filename format: `order_YYYYMMDD_HHMMSS_CustomerName.json`
   - Includes timestamp and order status

## How It Works

1. Customer starts conversation with the barista agent
2. Agent greets and asks what they'd like to order
3. Agent collects information through natural conversation:
   - Drink type (latte, cappuccino, americano, etc.)
   - Size (small, medium, large)
   - Milk preference (whole, skim, oat, almond, soy, none)
   - Any extras (whipped cream, extra shot, syrups)
   - Customer name
4. Once all information is collected, agent uses `save_order()` tool
5. Order is saved to JSON file with timestamp
6. Agent confirms the order with a friendly summary

## Testing the Agent

1. Make sure all services are running:
   ```bash
   # LiveKit Server
   .\livekit-server.exe --dev
   
   # Backend Agent
   cd backend
   uv run python src/agent.py dev
   
   # Frontend
   cd frontend
   pnpm dev
   ```

2. Open http://localhost:3000 in your browser

3. Try ordering:
   - "Hi, I'd like a large latte with oat milk"
   - "Can I add whipped cream and an extra shot?"
   - "My name is Alex"

4. Check `backend/orders/` for saved order JSON files

## Files Modified

- `backend/src/agent.py` - Main agent implementation with tools and order state

## Next Steps (Optional Advanced Challenge)

The advanced challenge would involve:
- Building HTML-based beverage visualization
- Dynamic cup size rendering
- Visual representation of extras (whipped cream, etc.)
- Order receipt rendering
- Using LiveKit data streams or RPC for real-time updates

## Primary Goal (Required)
Persona: Turn the agent into a friendly barista for a coffee brand of your choice.
Order state: Maintain a small order state object:
{
  "drinkType": "string",
  "size": "string",
  "milk": "string",
  "extras": ["string"],
  "name": "string"
}
Behavior:
The agent should ask clarifying questions until all fields in the order state are filled.
Once the order is complete, save the order to a JSON file summarizing the order.
