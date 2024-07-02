from django.shortcuts import render
from django.utils.timezone import datetime, timedelta
from openai import OpenAI
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
import pytz

from .models import ChatMessage
from .models import Temperature
from .serializers import TemperatureSerializer, ChatMessageSerializer


def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')


def data_view(request):
    return render(request, 'dashboard/date.html')


def chat_view(request):
    return render(request, 'dashboard/chat.html')


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 10  # Adjust as per your needs


class TemperatureListAPIView(generics.ListAPIView):
    serializer_class = TemperatureSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Temperature.objects.all()

        # Filter by date type (hour, day, month)
        filter_type = self.request.query_params.get('filter', None)
        if filter_type == 'hour':
            queryset = queryset.filter(date__gte=datetime.now() - timedelta(hours=1))
        elif filter_type == 'day':
            queryset = queryset.filter(date__gte=datetime.now() - timedelta(days=1))
        elif filter_type == 'month':
            queryset = queryset.filter(date__gte=datetime.now() - timedelta(days=30))

        # Sort by specified field (type, temperature, date)
        sort_by = self.request.query_params.get('sort_by', 'date')
        if sort_by in ['type', 'temperature', 'date']:
            queryset = queryset.order_by(sort_by)

        return queryset


class RecentTemperatureListAPIView(generics.ListAPIView):
    serializer_class = TemperatureSerializer

    def get_queryset(self):
        one_hour_ago = datetime.now() - timedelta(hours=1)
        return Temperature.objects.filter(date__gte=one_hour_ago)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            mock_data = [
                {"type": "outside", "temperature": 20.5, "date": "01:00"},
                {"type": "outside", "temperature": 24.5, "date": "01:10"},
                {"type": "outside", "temperature": 38.5, "date": "01:20"},
                {"type": "outside", "temperature": 30.5, "date": "01:30"},
                {"type": "inside", "temperature": 22.2, "date": "01:00"},
                {"type": "inside", "temperature": 21.1, "date": "01:10"},
                {"type": "inside", "temperature": 20.2, "date": "01:20"},
                {"type": "inside", "temperature": 26.4, "date": "01:30"},
            ]
            return Response(mock_data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ChatbotAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            temperatures = Temperature.objects.all()
            serializer = TemperatureSerializer(temperatures, many=True)

            user_prompt = request.data.get('message', '')
            chatbot_prompt = (f"Based on this data: {serializer.data} and the user prompt: {user_prompt}, "
                              f"respond to him please and give some advices and please answer in the language that the"
                              f"user asked. ( Most of the time is in Romanian. )")
            client = OpenAI(
                # This is the default and can be omitted
                api_key='sk-proj-GsUdSltxg8DOrtKYXr3jT3BlbkFJrvdppdLQOgvPPpAtkH8e',
            )

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": chatbot_prompt,
                    }
                ],
                model="gpt-3.5-turbo",
            )
            answer = chat_completion.choices[0].message.content
            print(f"ChatGPT: {answer}")

            # Salvează mesajul în baza de date (opțional, depinde de necesități)
            chat_message = ChatMessage.objects.create(prompt=chatbot_prompt, response=answer)
            chat_message.save()

            # Serializează răspunsul pentru a-l returna către client
            serializer = ChatMessageSerializer(chat_message)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeviceDataAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = TemperatureSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WelcomeMessageAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            tz = pytz.timezone('Europe/Bucharest')
            date_now = datetime.now(tz=tz).strftime("%Y-%m-%d")
            temperatures = Temperature.objects.filter(date__contains=date_now)

            if not temperatures:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = TemperatureSerializer(temperatures, many=True)

            chatbot_prompt = (
                f"Based on this data: {serializer.data} predict the weather and give some advice for the user in Romanian "
                f"please and do not mention about that I gave you data or anything about user.")

            client = OpenAI(
                # This is the default and can be omitted
                api_key='sk-proj-GsUdSltxg8DOrtKYXr3jT3BlbkFJrvdppdLQOgvPPpAtkH8e',
            )

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": chatbot_prompt,
                    }
                ],
                model="gpt-3.5-turbo",
            )
            answer = chat_completion.choices[0].message.content
            print(f"ChatGPT: {answer}")

            # Salvează mesajul în baza de date (opțional, depinde de necesități)
            chat_message = ChatMessage.objects.create(prompt=chatbot_prompt, response=answer)
            chat_message.save()

            # Serializează răspunsul pentru a-l returna către client
            serializer = ChatMessageSerializer(chat_message)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
