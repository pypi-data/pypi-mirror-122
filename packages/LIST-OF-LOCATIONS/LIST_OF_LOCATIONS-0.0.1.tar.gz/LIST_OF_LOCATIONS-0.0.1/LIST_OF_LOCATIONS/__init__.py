import asyncio
import techmanpy


speed = 0.00000001
robot_ip='192.168.10.9'

# async def getvalue(value):                                                              #Getting the robot location
#     async with techmanpy.connect_svr(robot_ip='192.168.10.9') as conn:
#        robot_model = await conn.get_value(value)
#        print(robot_model)


async def setvalue(key, value):                                                         #controling the gripper
   async with techmanpy.connect_svr(robot_ip='192.168.10.9') as conn:
      await conn.set_value(key,value)


# async def moveJ(j1,j2,j3,j4,j5,j6,v):                                                 #Robot movement move J
#    async with techmanpy.connect_sct(robot_ip=robot_ip) as conn:
#       await conn.move_to_joint_angles_ptp([j1, j2, j3, j4, j5, j6], v, 300)

async def moveJ_path(j1,j2,j3,j4,j5,j6,v):                                              #Robot movement move J in path
   async with techmanpy.connect_sct(robot_ip=robot_ip) as conn:
      await conn.move_to_joint_angles_path([j1, j2, j3, j4, j5, j6], v, 300)
      await conn.set_queue_tag(1,True)