from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password", "image", "code", "phone", "old_password")
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "code": {"read_only": True},
            "email": {"read_only": True},
            "phone": {"allow_null": True, "required": False},
            "username": {"read_only": True},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        old_password = validated_data.pop("old_password", None)
        image = validated_data.pop("image", None)

        # Mise à jour des champs simples
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Changement de mot de passe
        if password:
            if not old_password:
                raise serializers.ValidationError({
                    "old_password": "Mot de passe actuel requis."
                })

            if not instance.check_password(old_password):
                raise serializers.ValidationError({
                    "old_password": "Mot de passe actuel incorrect."
                })

            instance.set_password(password)

        # Gestion de l'image
        if image is not None:
            if instance.image:
                instance.image.delete(save=False)
            instance.image = image

        instance.save()
        return instance

