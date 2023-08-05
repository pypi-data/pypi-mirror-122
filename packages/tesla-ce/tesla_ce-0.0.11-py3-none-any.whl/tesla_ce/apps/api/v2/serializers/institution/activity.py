#  Copyright (c) 2020 Xavier Baró
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU Affero General Public License as
#      published by the Free Software Foundation, either version 3 of the
#      License, or (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU Affero General Public License for more details.
#
#      You should have received a copy of the GNU Affero General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
""" Activity serializer module """
from rest_framework import serializers

from tesla_ce.models import Activity


class InstitutionCourseActivitySerializer(serializers.ModelSerializer):
    """Activity serialize model module."""

    vle_activity_type = serializers.ReadOnlyField()
    vle_activity_id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    start = serializers.ReadOnlyField()
    end = serializers.ReadOnlyField()
    description = serializers.ReadOnlyField()

    class Meta:
        model = Activity
        exclude = ["vle", "course"]
