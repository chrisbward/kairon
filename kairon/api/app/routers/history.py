import os
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import FileResponse
from kairon.api.auth import Authentication
from kairon.data_processor.history import ChatHistory
from kairon.api.models import Response, User, HistoryMonth
from fastapi import Depends, Query
from typing import Text
from kairon.utils import Utility
router = APIRouter()


@router.get("/users", response_model=Response)
async def chat_history_users(month: HistoryMonth = 1, current_user: User = Depends(Authentication.get_current_user_and_bot)):

    """
    Fetches the list of user who has conversation with the agent
    """
    users, message = ChatHistory.fetch_chat_users(current_user.get_bot(), month)
    return {"data": {"users": users}, "message": message}


@router.get("/users/{sender}", response_model=Response)
async def chat_history(
    sender: Text, month: HistoryMonth = 1, current_user: User = Depends(Authentication.get_current_user_and_bot)
):
    """
    Fetches the list of conversation with the agent by particular user
    """
    history, message = ChatHistory.fetch_chat_history(current_user.get_bot(), sender, month)
    return {"data": {"history": list(history)}, "message": message}


@router.get("/metrics/users", response_model=Response)
async def user_with_metrics(
        month: HistoryMonth = 1, current_user: User = Depends(Authentication.get_current_user_and_bot)):
    """
    Fetches the list of user who has conversation with the agent with steps anf time
    """
    users, message = ChatHistory.user_with_metrics(
        current_user.get_bot(), month
    )
    return {"data": {"users": users}, "message": message}


@router.get("/metrics/fallback", response_model=Response)
async def visitor_hit_fallback(month: HistoryMonth = 1, current_user: User = Depends(Authentication.get_current_user_and_bot)):
    """
    Fetches the number of times the agent hit a fallback (ie. not able to answer) to user queries
    """
    visitor_hit_fallback, message = ChatHistory.visitor_hit_fallback(
        current_user.get_bot(), month
    )
    return {"data": visitor_hit_fallback, "message": message}


@router.get("/metrics/conversation/steps", response_model=Response)
async def conversation_steps(month: HistoryMonth = 1, current_user: User = Depends(Authentication.get_current_user_and_bot)):
    """
     Fetches the number of conversation steps that took place in the chat between the users and the agent
     """
    conversation_steps, message = ChatHistory.conversation_steps(current_user.get_bot(), month)
    return {"data": conversation_steps, "message": message}


@router.get("/metrics/conversation/time", response_model=Response)
async def conversation_time(month: HistoryMonth = 1,current_user: User = Depends(Authentication.get_current_user_and_bot)):
    """
    Fetches the duration of the chat that took place between the users and the agent"""
    conversation_time, message = ChatHistory.conversation_time(current_user.get_bot(), month)
    return {"data": conversation_time, "message": message}


@router.get("/metrics/user/engaged", response_model=Response)
async def count_engaged_users(month: int = 1, conversation_step_threshold: int = 10,
                              current_user: User = Depends(Authentication.get_current_user_and_bot)):

    """
    Fetches the number of engaged users of the bot
    """
    engaged_user_count, message = ChatHistory.engaged_users(
        current_user.get_bot(), month, conversation_step_threshold
    )
    return {"data": engaged_user_count, "message": message}


@router.get("/metrics/user/new", response_model=Response)
async def count_new_users(month: HistoryMonth = 1, current_user: User = Depends(Authentication.get_current_user_and_bot)):
    """
    Fetches the number of new users of the bot
    """
    user_count, message = ChatHistory.new_users(
        current_user.get_bot(), month
    )
    return {"data": user_count, "message": message}


@router.get("/metrics/conversation/success", response_model=Response)
async def complete_conversations(month: HistoryMonth = 1, current_user: User = Depends(Authentication.get_current_user_and_bot)):
    """
    Fetches the number of successful conversations of the bot, which had no fallback
    """
    conversation_count, message = ChatHistory.successful_conversations(
        current_user.get_bot(), month
    )
    return {"data": conversation_count, "message": message}


@router.get("/metrics/user/retention", response_model=Response)
async def calculate_retention(month: HistoryMonth = 1, current_user: User = Depends(Authentication.get_current_user_and_bot)):
    """
    Fetches the user retention percentage of the bot
    """
    retention_count, message = ChatHistory.user_retention(
        current_user.get_bot(), month
    )
    return {"data": retention_count, "message": message}


@router.get("/metrics/trend/user/engaged", response_model=Response)
async def engaged_users_trend(month: int = Query(default=6, ge=2, le=6),
                              conversation_step_threshold: int = 10,
                              current_user: User = Depends(Authentication.get_current_user_and_bot)):

    """
    Fetches the counts of engaged users of the bot for previous months
    """
    range_value, message = ChatHistory.engaged_users_range(
        current_user.get_bot(), month, conversation_step_threshold
    )
    return {"data": range_value, "message": message}


@router.get("/metrics/trend/user/new", response_model=Response)
async def new_users_trend(month: int = Query(default=6, ge=2, le=6), current_user: User = Depends(Authentication.get_current_user_and_bot)):
    """
    Fetches the counts of new users of the bot for previous months
    """
    range_value, message = ChatHistory.new_users_range(
        current_user.get_bot(), month
    )
    return {"data": range_value, "message": message}


@router.get("/metrics/trend/conversation/success", response_model=Response)
async def complete_conversation_trend(month: int = Query(default=6, ge=2, le=6), current_user: User = Depends(Authentication.get_current_user_and_bot)):
    """
    Fetches the counts of successful conversations of the bot for previous months
    """
    range_value, message = ChatHistory.successful_conversation_range(
        current_user.get_bot(), month
    )
    return {"data": range_value, "message": message}


@router.get("/metrics/trend/user/retention", response_model=Response)
async def retention_trend(month: int = Query(default=6, ge=2, le=6), current_user: User = Depends(Authentication.get_current_user_and_bot)):
    """
    Fetches the counts of user retention percentages of the bot for previous months
    """
    range_value, message = ChatHistory.user_retention_range(
        current_user.get_bot(), month
    )
    return {"data": range_value, "message": message}


@router.get("/metrics/trend/user/fallback", response_model=Response)
async def fallback_trend(month: int = Query(default=6, ge=2, le=6), current_user: User = Depends(Authentication.get_current_user_and_bot)):
    """
    Fetches the fallback count of the bot for previous months
    """
    range_value, message = ChatHistory.fallback_count_range(
        current_user.get_bot(), month
    )
    return {"data": range_value, "message": message}


@router.get("/conversations", response_model=Response)
async def flat_conversations(month: int = Query(default=1, ge=1, le=6), current_user: User = Depends(Authentication.get_current_user_and_bot)):
    """
    Fetches the flattened conversation data of the bot for previous months
    """
    flat_data, message = ChatHistory.flatten_conversations(
        current_user.get_bot(), month
    )
    return {"data": flat_data, "message": message}


@router.get("/conversations/download")
async def download_conversations(
        background_tasks: BackgroundTasks,
        month: int = Query(default=1, ge=1, le=6),
        current_user: User = Depends(Authentication.get_current_user_and_bot),
):
    """
    Downloads conversation history of the bot, for the specified months
    """
    conversation_data, message = ChatHistory.flatten_conversations(current_user.get_bot(), month)
    file, temp_path = Utility.download_csv(conversation_data, message)
    response = FileResponse(
        file, filename=os.path.basename(file), background=background_tasks
    )
    response.headers[
        "Content-Disposition"
    ] = "attachment; filename=" + os.path.basename(file)
    background_tasks.add_task(Utility.delete_directory, temp_path)
    return response
