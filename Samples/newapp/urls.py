from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('adm_home/',views.adm_home),
    path('comp_home/',views.comp_home),
    path('worker_home/',views.worker_home),
    path('login_load/',views.login_load),
    path('logout/',views.logout),
    path('company_registration_load/',views.company_registration_load),
    path('company_registration_post/',views.company_registration_post),
    path('worker_reg_post/',views.worker_reg_post),
    path('worker_reg_load/',views.worker_reg_load),


    path('worker_reg_index/',views.worker_reg_index),


###ADMIN START
    path('admin_addskill_load/',views.admin_addskill_load),
    path('admin_editskill_load/<skill_id>',views.admin_editskill_load),
    path('admin_viewskill_load/',views.admin_viewskill_load),

    path('admin_delete_skill/<skill_id>',views.admin_delete_skill),

    path('admin_view_registered_companies_and_approval/',views.admin_view_registered_companies_and_approval),

    path('admin_approve_worker/<login_id>',views.admin_approve_worker),
    path('admin_reject_worker/<login_id>',views.admin_reject_worker),
    path('admin_block_worker/<login_id>',views.admin_block_worker),
    path('admin_unblock_worker/<login_id>',views.admin_unblock_worker),
    path('admin_block_worker_by_request/<login_id>/<request_id>',views.admin_block_worker_by_request),
    path('admin_block_company/<login_id>',views.admin_block_company),
    path('admin_unblock_company/<login_id>',views.admin_unblock_company),


    path('admin_view_approved_companies/',views.admin_view_approved_companies),
    path('admin_view_rejected_companies/',views.admin_view_rejected_companies),
    path('admin_view_registered_workers_and_approval/',views.admin_view_registered_workers_and_approval),
    path('admin_view_approved_worker/',views.admin_view_approved_worker),
    path('admin_view_rejected_worker/',views.admin_view_rejected_worker),
    path('admin_view_block_request_from_user/',views.admin_view_block_request_from_user),
    path('admin_view_complaint_from_user/',views.admin_view_complaint_from_user),
    path('admin_send_reply/<complaint_id>/',views.admin_send_reply),
    path('admin_view_feedback_worker/',views.admin_view_feedback_worker),
    path('admin_view_feedback_company/',views.admin_view_feedback_company),

    ##  admin post
    path('login_post/',views.login_post),
    path('admin_addskill_load_post/',views.admin_addskill_load_post),
    path('admin_editskill_load_post/',views.admin_editskill_load_post),
    path('admin_viewskill_load_post/',views.admin_viewskill_load_post),
    path('admin_viewregistered_companies_and_approval_post/',views.admin_viewregistered_companies_and_approval_post),
    
    path('admin_approve_company/<login_id>',views.admin_approve_company),
    path('admin_reject_company/<login_id>',views.admin_reject_company),

    path('admin_view_approved_companies_post/',views.admin_view_approved_companies_post),
    path('admin_view_rejected_companies_post/',views.admin_view_rejected_companies_post),
    path('admin_view_registered_workers_and_approval_post/',views.admin_view_registered_workers_and_approval_post),
    path('admin_view_approved_worker_post/',views.admin_view_approved_worker_post),
    path('admin_view_rejected_worker_post/',views.admin_view_rejected_worker_post),
    path('admin_view_block_request_from_user_post/',views.admin_view_block_request_from_user_post),
    path('admin_view_complaint_from_user_post/',views.admin_view_complaint_from_user_post),
    path('admin_send_reply_post/',views.admin_send_reply_post),
    path('admin_view_feedback_worker_post/',views.admin_view_feedback_worker_post),
    path('admin_view_feedback_company_post/',views.admin_view_feedback_company_post),


###COMPANY START
    path('company_view_profile/',views.company_view_profile),
    path('company_edit_profile/',views.company_edit_profile),
    path('add_vaccancy/',views.add_vaccancy),
    path('view_vaccancy/',views.view_vaccancy),
    path('company_edit_view_vaccancy/<vaccancy_id>',views.company_edit_view_vaccancy),
    path('company_edit_view_vaccancy_post/',views.company_edit_view_vaccancy_post),
    path('company_delete_vaccancy/<vaccancy_id>',views.company_delete_vaccancy),

    path('skill_management/<vaccancy_id>',views.skill_management),
    path('skill_management_post/',views.skill_management_post),
    path('company_delete_skill/<vaccancy_skill_id>/<vid>',views.company_delete_skill),

    path('view_vaccancy_request_from_user/',views.view_vaccancy_request_from_user),
    path('view_vaccancy_request_from_user2/<wid>/<reqid>',views.view_vaccancy_request_from_user2),
    path('view_approved_vaccancy/',views.view_approved_vaccancy),
    path('view_approved_vaccancy2/<wid>/<reqid>',views.view_approved_vaccancy2),
    path('view_feedback_from_worker/',views.view_feedback_from_worker),


###COMPANY POST
    path('company_view_profile_post/', views.company_view_profile_post),
    path('company_edit_profile_post/', views.company_edit_profile_post),
    path('add_vaccancy_post/', views.add_vaccancy_post),
    path('view_vaccancy_post/', views.view_vaccancy_post),
    path('view_vaccancy_request_from_user_post/', views.view_vaccancy_request_from_user_post),
    path('view_vaccancy_request_from_user2_post/', views.view_vaccancy_request_from_user2_post),
    path('view_approved_vaccancy_post/', views.view_approved_vaccancy_post),
    # path('view_approved_vaccancy2_post/', views.view_approved_vaccancy2_post),
    path('view_feedback_from_worker_post/', views.view_feedback_from_worker_post),



###START WORKERS
    
    path('workers_view_profile/', views.workers_view_profile),
    path('workers_edit_profile/', views.workers_edit_profile),
    path('workers_add_skill/', views.workers_add_skill),
    path('worker_delete_skill/<worker_skill_id>',views.worker_delete_skill),
    path('workers_upload_previous_works/', views.workers_upload_previous_works),
    path('workers_view_previous_works/', views.workers_view_previous_works),
    path('workers_upload_resume/', views.workers_upload_resume),
    path('workers_send_complaint/', views.workers_send_complaint),
    path('workers_view_complaint_reply/', views.workers_view_complaint_reply),
    path('workers_view_vaccancy_and_send_request/',views.workers_view_vaccancy_and_send_request),
    path('worker_sent_vaccancy_request/<vaccancy_id>',views.worker_sent_vaccancy_request),
    path('workers_view_sent_vaccancy_request/', views.workers_view_sent_vaccancy_request),
    path('worker_delete_sent_vaccancy_request/<vaccancy_id>',views.worker_delete_sent_vaccancy_request),
    path('workers_view_user_request_and_approval/', views.workers_view_user_request_and_approval),
    path('workers_approve_user_request/<request_id>',views.workers_approve_user_request),
    path('wokers_view_payment_details/<work_request_id>',views.wokers_view_payment_details),
    path('workers_reject_user_request/<request_id>',views.workers_reject_user_request),
    path('workers_chat_with_user/<userid>', views.workers_chat_with_user),
    path('workersviewmsg/', views.workersviewmsg),
    path('workers_insert_chat/<msg>', views.workers_insert_chat),
    path('workers_send_feedback/<comp_lid>', views.workers_send_feedback),
    path('workers_send_feedback_about_companies/', views.workers_send_feedback_about_companies),
    path('workers_view_feedback_from_user/', views.workers_view_feedback_from_user),

###WORKER POST
    path('workers_view_profile_post/', views.workers_view_profile_post),
    path('workers_edit_profile_post/', views.workers_edit_profile_post),
    path('workers_add_skill_post/', views.workers_add_skill_post),
    path('workers_upload_previous_works_post/', views.workers_upload_previous_works_post),


    path('workers_upload_work_images/<work_id>', views.workers_upload_work_images),
    path('workers_upload_work_images_post/', views.workers_upload_work_images_post),
    path('workers_remove_work_images_post/<work_image_id>', views.workers_remove_work_images_post),



    path('workers_delete_previous_works/<work_id>', views.workers_delete_previous_works),
    path('workers_upload_resume_post/', views.workers_upload_resume_post),
    path('workers_send_complaint_post/', views.workers_send_complaint_post),
    path('workers_view_complaint_reply_post/', views.workers_view_complaint_reply_post),
    path('worker_delete_complaint/<complaint_id>',views.worker_delete_complaint),
    path('workers_view_vaccancy_and_send_request_post/', views.workers_view_vaccancy_and_send_request_post),
    path('workers_view_user_request_and_approval_post/', views.workers_view_user_request_and_approval_post),
    path('workers_send_feedback_post/', views.workers_send_feedback_post),
    path('workers_send_feedback_about_companies_post/', views.workers_send_feedback_about_companies_post),
    path('workers_view_feedback_from_user_post/', views.workers_view_feedback_from_user_post),


    path('forgot_load/',views.forgot_load),
    path('forgot_post/',views.forgot_post),
    # path('f2/<int:c>',views.cube),
    # path('f3/<int:x>/<int:y>',views.large),
    # path('f4/',views.input_no),
    # path('f5/',views.submit),
    # path('f6/',views.first_get),
    # path('f7/',views.first_post),



        ############### android
        path('and_login/', views.and_login),
        path('and_forgot_password/', views.and_forgot_password),
        path('and_signup/',views.and_signup),
        path('and_view_profile/',views.and_view_profile),
        path('and_update_profile/',views.and_update_profile),
        path('and_view_workers/',views.and_view_workers),
        path('and_view_previous_works/',views.and_view_previous_works),
        path('and_request_work/',views.and_request_work),
        path('and_view_request_status/',views.and_view_request_status),
        path('and_payment/',views.and_payment),
        path('and_delete_request/',views.and_delete_request),
        path('and_send_feedback/',views.and_send_feedback),
        path('and_view_feedback/',views.and_view_feedback),
        path('and_send_complaint/',views.and_send_complaint),
        path('and_view_complaint_reply/',views.and_view_complaint_reply),
        path('and_delete_complaint/',views.and_delete_complaint),
        path('and_send_block_request/',views.and_send_block_request),
        path('and_delete_block_request/',views.and_delete_block_request),
        path('and_view_block_request_status/',views.and_view_block_request_status),
        path('inmessage/',views.inmessage),
        path('view_message2/',views.view_message2),
        path('and_view_all_skill/',views.and_view_all_skill),
        path('and_view_workers_by_skill/',views.and_view_workers_by_skill),
        path('and_view_works_homepage/',views.and_view_works_homepage),
        path('and_get_request_notification/',views.and_get_request_notification),
        path('and_update_request_seen_status/',views.and_update_request_seen_status),
        path('and_view_works_images/',views.and_view_works_images),
        path('and_get_chat_notification/',views.and_get_chat_notification),
        path('and_search_category_or_works/',views.and_search_category_or_works),
        path('and_ratings/',views.and_ratings),

        


]
