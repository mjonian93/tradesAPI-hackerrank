from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Trade
from .serializers import TradeSerializer

# Create your views here.

class TradesAPIView(APIView):
    allowed_methods = ['POST', 'GET', 'DELETE']

    def post(self, request):
        #check values
        type = request.data.get('type')
        shares = int(request.data.get('shares'))

        if shares not in range(1, 100):
            return Response({"status": "Bad Request", "data": "Shares value not within expected range"},
                            status=status.HTTP_400_BAD_REQUEST)
        if type not in ['buy', 'sell']:
            return Response({"status": "Bad Request", "data": "Type value not recognized."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = TradeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            trade = get_object_or_404(Trade, id=id)
            serializer = TradeSerializer(trade)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        if self.request.query_params:
            return self.get_queryset()
        else:
            trades = Trade.objects.all()
            serializer = TradeSerializer(trades, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def get_queryset(self):
        trade_type = self.request.query_params.get('type')
        user_id = self.request.query_params.get('user_id')

        if trade_type not in ['buy', 'sell']:
            return Response({"status": "Bad Request", "data": "Type value not recognized."},
                            status=status.HTTP_400_BAD_REQUEST)

        trade = get_object_or_404(Trade, type=trade_type, user_id=user_id)
        serializer = TradeSerializer(trade)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, id=None):
        trade = get_object_or_404(Trade, id=id)
        trade.delete()
        return Response({"status": "success", "data": "Item Deleted"}, status=status.HTTP_204_NO_CONTENT)

