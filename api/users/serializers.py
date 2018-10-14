from django.contrib.auth.models import Group, User
from django.contrib.auth.hashers import make_password
from users.models import UserPlayer
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups',  'password')
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password']),
        )

        groups_data = validated_data.pop('groups')

        for group in groups_data:
                user.groups.add(group)

        user.save()
        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class UserPlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, required=True)

    class Meta:
        model = UserPlayer
        fields = ('user', 'xp')

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        player, created = UserPlayer.objects.update_or_create(user=user,
                            xp=validated_data.pop('xp'))
        return player