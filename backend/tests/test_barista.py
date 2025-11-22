import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from livekit.agents import RunContext
from livekit import rtc
from agent import Assistant

@pytest.fixture
def mock_room():
    room = MagicMock(spec=rtc.Room)
    room.local_participant = MagicMock()
    room.local_participant.publish_data = AsyncMock()
    return room

@pytest.fixture
def assistant(mock_room):
    return Assistant(room=mock_room)

@pytest.fixture
def mock_context():
    return MagicMock(spec=RunContext)

@pytest.mark.asyncio
async def test_initial_state(assistant):
    assert assistant.order_state["drinkType"] is None
    assert assistant.order_state["size"] is None
    assert assistant.order_state["milk"] is None
    assert assistant.order_state["extras"] == []
    assert assistant.order_state["name"] is None

@pytest.mark.asyncio
async def test_update_drink_type(assistant, mock_context):
    result = await assistant.update_drink_type(mock_context, "Latte")
    assert assistant.order_state["drinkType"] == "latte"
    assert "latte" in result.lower()
    # Verify publish called
    assistant.room.local_participant.publish_data.assert_called()

@pytest.mark.asyncio
async def test_update_size(assistant, mock_context):
    # Valid size
    result = await assistant.update_size(mock_context, "Large")
    assert assistant.order_state["size"] == "large"
    assert "large" in result.lower()
    assistant.room.local_participant.publish_data.assert_called()
    
    # Invalid size
    result = await assistant.update_size(mock_context, "Huge")
    assert assistant.order_state["size"] == "large" # Should not change
    assert "choose small, medium, or large" in result.lower()

@pytest.mark.asyncio
async def test_update_milk(assistant, mock_context):
    result = await assistant.update_milk(mock_context, "Oat")
    assert assistant.order_state["milk"] == "oat"
    assert "oat" in result.lower()
    assistant.room.local_participant.publish_data.assert_called()

@pytest.mark.asyncio
async def test_add_extras(assistant, mock_context):
    await assistant.add_extra(mock_context, "Whipped Cream")
    assert "whipped cream" in assistant.order_state["extras"]
    assistant.room.local_participant.publish_data.assert_called()
    
    await assistant.add_extra(mock_context, "Vanilla Syrup")
    assert "vanilla syrup" in assistant.order_state["extras"]
    assert len(assistant.order_state["extras"]) == 2
    
    # Duplicate check
    result = await assistant.add_extra(mock_context, "Whipped Cream")
    assert len(assistant.order_state["extras"]) == 2
    assert "already in your order" in result.lower()

@pytest.mark.asyncio
async def test_update_name(assistant, mock_context):
    await assistant.update_name(mock_context, "Alice")
    assert assistant.order_state["name"] == "Alice"
    assistant.room.local_participant.publish_data.assert_called()

@pytest.mark.asyncio
async def test_save_order_incomplete(assistant, mock_context):
    # Only name set
    assistant.order_state["name"] = "Bob"
    result = await assistant.save_order(mock_context)
    assert "Cannot save order yet" in result
    assert "missing" in result

@pytest.mark.asyncio
async def test_save_order_complete(assistant, mock_context):
    # Fill all fields
    assistant.order_state["drinkType"] = "mocha"
    assistant.order_state["size"] = "medium"
    assistant.order_state["milk"] = "whole"
    assistant.order_state["name"] = "Charlie"
    
    # Mock file writing to avoid actual file creation during tests
    with patch("builtins.open", new_callable=MagicMock) as mock_open:
        result = await assistant.save_order(mock_context)
        
        assert "Order confirmed" in result
        assert "Charlie" in result
        assert mock_open.called
        # Verify final publish
        assistant.room.local_participant.publish_data.assert_called()

@pytest.mark.asyncio
async def test_html_generation(assistant):
    assistant.order_state["drinkType"] = "latte"
    assistant.order_state["size"] = "small"
    assistant.order_state["name"] = "Dave"
    
    html = assistant._generate_html()
    assert "latte" in html
    assert "Dave" in html
    assert "120px" in html # Small size height
