from rest_framework.views import APIView
from apps.inform.models import Inform, InformRead
from apps.inform.serializers import InformSerializer
from django.db.models import Q
from django.db.models import Prefetch
from rest_framework.response import Response
from apps.absent.models import Absent
from apps.absent.serializers import AbsentSerializer
from apps.oaauth.models import OADepartment
from django.db.models import Count
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class LatestInformView(APIView):
    """
    返回最新的10条通知
    """
    # 这里的cache_page是缓存15分钟，也就是15分钟内发布新的通知，不会立即显示
    # @method_decorator(cache_page(60 * 15))
    def get(self, request):
        current_user = request.user
        # 返回公共的，或者是所在的部门能看到的通知
        informs = Inform.objects.prefetch_related(
            Prefetch(
                "reads", queryset=InformRead.objects.filter(user_id=current_user.uid)
            ),
            "departments",
        ).filter(Q(public=True) | Q(departments=current_user.department))[:10]
        serializer = InformSerializer(informs, many=True)
        return Response(serializer.data)


class LatestAbsentView(APIView):

    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        # 董事会的人，可以看到所有人的考勤信息，非董事会的人，只能看到自己部门的考勤信息
        current_user = request.user
        queryset = Absent.objects
        if current_user.department.name != "董事会":
            queryset = queryset.filter(
                requester__department_id=current_user.department_id
            )
        queryset = queryset.all()[:10]
        serializer = AbsentSerializer(queryset, many=True)
        return Response(serializer.data)


class DepartmentStaffCountView(APIView):

    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        rows = OADepartment.objects.annotate(staff_count=Count("staffs")).values(
            "name", "staff_count"
        )
        print("=" * 10)
        return Response(rows)


class HealthCheckView(APIView):
    def get(self, request):
        return Response({"code": 200})