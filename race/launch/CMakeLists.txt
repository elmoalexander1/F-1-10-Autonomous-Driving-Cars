<launch>
  <node pkg="race" name="keyboard.py" type="keyboard.py"/>
  <node pkg="race" name="talker.py" type="talker.py" output="screen"/>
</launch>
