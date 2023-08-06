import open3d as o3d
import numpy as np
import copy
import cv2
import time
import os


# from numba import cuda
# #检测一下GPU是否可用
# print(cuda.gpus)
from hito.func.engine.hitoFunc import HitoFunc


def draw_registration_result(source, target, transformation):
    source_temp = source.clone()
    target_temp = target.clone()
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries(
        [source_temp.to_legacy(),
         target_temp.to_legacy()],
        # zoom=0.4459,
        # front=[0.9288, -0.2951, -0.2242],
        # lookat=[1.6784, 2.0612, 1.4451],
        # up=[-0.3402, -0.9189, -0.1996])
    )


# source = o3d.t.io.read_point_cloud('cloud_bin_0.pcd')
# target = o3d.t.io.read_point_cloud('cloud_bin_1.pcd')


def multi_scale_icp_registration(source, target, max_iteration=50, relative_fitness=0.0001, relative_rmse=0.0001):
    voxel_sizes = o3d.utility.DoubleVector([0.1, 0.05, 0.025, 0.0125])

    # List of Convergence-Criteria for Multi-Scale ICP:
    criteria_list = [
        o3d.t.pipelines.registration.ICPConvergenceCriteria(relative_rmse,
                                                            relative_fitness,
                                                            max_iteration),
        o3d.t.pipelines.registration.ICPConvergenceCriteria(0.00001, 0.00001, 15),
        o3d.t.pipelines.registration.ICPConvergenceCriteria(0.000001, 0.000001, 10),
        o3d.t.pipelines.registration.ICPConvergenceCriteria(0.0000001, 0.0000001, 5)
    ]

    # `max_correspondence_distances` for Multi-Scale ICP (o3d.utility.DoubleVector):
    # max_correspondence_distances = o3d.utility.DoubleVector([10000.0, 10000.0, 10000.0])
    max_correspondence_distances = o3d.utility.DoubleVector([0.3, 0.14, 0.07, 0.035])
    # Initial alignment or source to target transform.
    init_source_to_target = o3d.core.Tensor.eye(4, o3d.core.Dtype.Float32)

    # Select the `Estimation Method`, and `Robust Kernel` (for outlier-rejection).
    # estimation = o3d.t.pipelines.registration.TransformationEstimationPointToPoint()
    estimation = o3d.t.pipelines.registration.TransformationEstimationPointToPoint()

    # Save iteration wise `fitness`, `inlier_rmse`, etc. to analyse and tune result.
    callback_after_iteration = lambda loss_log_map: print(
        "Iteration Index: {}, Scale Index: {}, Scale Iteration Index: {}, Fitness: {}, Inlier RMSE: {},".format(
            loss_log_map["iteration_index"].item(),
            loss_log_map["scale_index"].item(),
            loss_log_map["scale_iteration_index"].item(),
            loss_log_map["fitness"].item(),
            loss_log_map["inlier_rmse"].item()))
    voxel_size = 1
    # source_cuda = source.cuda(0)
    # target_cuda = target.cuda(0)
    source_down, target_down, source_fpfh, target_fpfh = voxel_down_and_get_fpfh(source, target, voxel_size)
    s = time.time()
    global_reg = execute_fast_global_registration(source_down.to_legacy(), target_down.to_legacy(), source_fpfh,
                                                  target_fpfh, voxel_size)
    global_reg_time = time.time() - s
    # print("global_reg:",global_reg.transformation)
    # print("global_time:",global_reg_time)
    init_source_to_target = o3d.core.Tensor(global_reg.transformation)
    registration_ms_icp = o3d.t.pipelines.registration.multi_scale_icp(source, target,
                                                                       voxel_sizes, criteria_list,
                                                                       max_correspondence_distances,
                                                                       init_source_to_target, estimation)

    return registration_ms_icp


def voxel_down_and_get_fpfh(source, target, voxel_size):
    radius_normal = voxel_size * 3

    source.estimate_normals(radius=radius_normal, max_nn=50)
    target.estimate_normals(radius=radius_normal, max_nn=50)

    source_down = source.voxel_down_sample(voxel_size=1)
    target_down = target.voxel_down_sample(voxel_size=1)

    radius_feature = voxel_size * 6
    source_fpfh = o3d.pipelines.registration.compute_fpfh_feature(source_down.to_legacy(),
                                                                  o3d.geometry.KDTreeSearchParamHybrid(
                                                                      radius=radius_feature, max_nn=100))
    target_fpfh = o3d.pipelines.registration.compute_fpfh_feature(target_down.to_legacy(),
                                                                  o3d.geometry.KDTreeSearchParamHybrid(
                                                                      radius=radius_feature, max_nn=100))
    return source_down, target_down, source_fpfh, target_fpfh


def execute_fast_global_registration(source_down, target_down, source_fpfh,
                                     target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5
    # print(":: 基于距离阈值为 %.3f的快速全局配准" % distance_threshold)
    result = o3d.pipelines.registration.registration_fgr_based_on_feature_matching(source_down, target_down,
                                                                                   source_fpfh, target_fpfh,
                                                                                   o3d.pipelines.registration.FastGlobalRegistrationOption(
                                                                                       maximum_correspondence_distance=distance_threshold))
    # result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
    #    source_down, target_down, source_fpfh, target_fpfh, True, distance_threshold,
    #    o3d.pipelines.registration.TransformationEstimationPointToPoint(False), 3,
    #    [o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
    #     o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(distance_threshold)
    #     ], o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.9))  # (100000, 0.999)                                                                                   maximum_correspondence_distance=distance_threshold))
    return result


def registration_icp(srouce, target):
    criteria = o3d.t.pipelines.registration.ICPConvergenceCriteria(relative_fitness=0.000001,
                                                                   relative_rmse=0.000001,
                                                                   max_iteration=50)
    # Initial alignment or source to target transform.
    init_source_to_target = np.asarray([[0.862, 0.011, -0.507, 0.5],
                                        [-0.139, 0.967, -0.215, 0.7],
                                        [0.487, 0.255, 0.835, -1.4],
                                        [0.0, 0.0, 0.0, 1.0]])
    max_correspondence_distance = 0.07
    voxel_size = 0.025
    result = o3d.t.pipelines.registration.icp(source, target, max_correspondence_distance,
                                              init_source_to_target, estimation, criteria,
                                              voxel_size, callback_after_iteration)
    return result


def Integ_test():
    files = os.listdir(r".\RH\tr")
    s = time.time()
    for file in files:
        # print(file)

        # print(file.replace('tr','ref'))
        source_file = ".\\RH\\tr\\" + file
        target_file = ".\\RH\\ref\\" + file.replace("tr", "ref")

        # print(source_file,target_file)
        try:
            source = o3d.t.io.read_point_cloud(source_file)

            target = o3d.t.io.read_point_cloud(target_file)

            registration_ms_icp = multi_scale_icp_registration(source, target, 100)
            if registration_ms_icp.fitness < 0.01:
                print("fitness<0.01", source_file)
        except:
            print(file)
    ms_icp_time = time.time() - s
    print("ms_icp_time", ms_icp_time)


def unit_test():
    s = time.time()
    source = o3d.t.io.read_point_cloud(r'..\..\RH\tr\pcd_tr_1-1_YGJ-bolt_1.pcd')
    target = o3d.t.io.read_point_cloud(r'..\..\RH\ref\pcd_ref_1-1_YGJ-bolt_1.pcd')
    registration_ms_icp = multi_scale_icp_registration(source, target, 100)
    ms_icp_time = time.time() - s
    if registration_ms_icp.fitness > 0.05:
        print("registration_ms_icp.fitness >0.05", registration_ms_icp.fitness)
    print("Time taken by Multi-Scale ICP: ", ms_icp_time)
    print("Inlier Fitness: ", registration_ms_icp.fitness)
    print("Inlier RMSE: ", registration_ms_icp.inlier_rmse)
    print("trasformation:", registration_ms_icp.transformation)
    draw_registration_result(source.cpu(), target.cpu(),
                             registration_ms_icp.transformation)


class MultiScaleIcpAlignFunc(HitoFunc):
    def process(self, source, target):
        registration_ms_icp=multi_scale_icp_registration(source, target, 100)
        return registration_ms_icp



if __name__ == '__main__':
    #Integ_test()
     unit_test()