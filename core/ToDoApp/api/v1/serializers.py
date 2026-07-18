from rest_framework import serializers, status

from ToDoApp.models import Task
from account.models import UserProfile, User


class TaskSerializer(serializers.ModelSerializer):
    abs_url = serializers.HyperlinkedIdentityField(
        view_name='Task-detail',
        read_only=True
    )
    class Meta:
        model = Task
        fields = ['id','user','title','description','status','abs_url','created_date','updated_date']
        read_only_fields = ['id','user','created_date','updated_date']

    # def get_url(self,obj):
    #     request = self.context.get('request')
    #     return request.build_absolute_uri(obj.pk)

    def create(self, validated_data):

        validated_data['user'] = UserProfile.objects.get(user=self.context['request'].user)

        if Task.objects.filter(user=validated_data['user'], title=validated_data['title'], status=True).exists():
            raise serializers.ValidationError('Task with this title already exists')

        return super().create(validated_data)
