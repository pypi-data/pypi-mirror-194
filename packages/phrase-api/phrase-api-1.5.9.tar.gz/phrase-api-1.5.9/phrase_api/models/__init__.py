# coding: utf-8

# flake8: noqa
"""
    Phrase Strings API Reference

    The version of the OpenAPI document: 2.0.0
    Contact: support@phrase.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

# import models into model package
from phrase_api.models.account import Account
from phrase_api.models.account_details import AccountDetails
from phrase_api.models.account_details1 import AccountDetails1
from phrase_api.models.account_search_result import AccountSearchResult
from phrase_api.models.affected_count import AffectedCount
from phrase_api.models.affected_resources import AffectedResources
from phrase_api.models.authorization import Authorization
from phrase_api.models.authorization_create_parameters import AuthorizationCreateParameters
from phrase_api.models.authorization_update_parameters import AuthorizationUpdateParameters
from phrase_api.models.authorization_with_token import AuthorizationWithToken
from phrase_api.models.authorization_with_token1 import AuthorizationWithToken1
from phrase_api.models.bitbucket_sync import BitbucketSync
from phrase_api.models.bitbucket_sync_export_parameters import BitbucketSyncExportParameters
from phrase_api.models.bitbucket_sync_export_response import BitbucketSyncExportResponse
from phrase_api.models.bitbucket_sync_import_parameters import BitbucketSyncImportParameters
from phrase_api.models.blacklisted_key import BlacklistedKey
from phrase_api.models.blacklisted_key_create_parameters import BlacklistedKeyCreateParameters
from phrase_api.models.blacklisted_key_update_parameters import BlacklistedKeyUpdateParameters
from phrase_api.models.branch import Branch
from phrase_api.models.branch_create_parameters import BranchCreateParameters
from phrase_api.models.branch_merge_parameters import BranchMergeParameters
from phrase_api.models.branch_name import BranchName
from phrase_api.models.branch_update_parameters import BranchUpdateParameters
from phrase_api.models.comment import Comment
from phrase_api.models.comment_create_parameters import CommentCreateParameters
from phrase_api.models.comment_mark_read_parameters import CommentMarkReadParameters
from phrase_api.models.comment_update_parameters import CommentUpdateParameters
from phrase_api.models.current_user import CurrentUser
from phrase_api.models.distribution import Distribution
from phrase_api.models.distribution_create_parameters import DistributionCreateParameters
from phrase_api.models.distribution_preview import DistributionPreview
from phrase_api.models.distribution_update_parameters import DistributionUpdateParameters
from phrase_api.models.document import Document
from phrase_api.models.format import Format
from phrase_api.models.github_sync_export_parameters import GithubSyncExportParameters
from phrase_api.models.github_sync_import_parameters import GithubSyncImportParameters
from phrase_api.models.gitlab_sync import GitlabSync
from phrase_api.models.gitlab_sync_export import GitlabSyncExport
from phrase_api.models.gitlab_sync_export_parameters import GitlabSyncExportParameters
from phrase_api.models.gitlab_sync_history import GitlabSyncHistory
from phrase_api.models.gitlab_sync_import_parameters import GitlabSyncImportParameters
from phrase_api.models.glossary import Glossary
from phrase_api.models.glossary_create_parameters import GlossaryCreateParameters
from phrase_api.models.glossary_term import GlossaryTerm
from phrase_api.models.glossary_term_create_parameters import GlossaryTermCreateParameters
from phrase_api.models.glossary_term_translation import GlossaryTermTranslation
from phrase_api.models.glossary_term_translation_create_parameters import GlossaryTermTranslationCreateParameters
from phrase_api.models.glossary_term_translation_update_parameters import GlossaryTermTranslationUpdateParameters
from phrase_api.models.glossary_term_update_parameters import GlossaryTermUpdateParameters
from phrase_api.models.glossary_update_parameters import GlossaryUpdateParameters
from phrase_api.models.icu import Icu
from phrase_api.models.icu_skeleton_parameters import IcuSkeletonParameters
from phrase_api.models.inline_response422 import InlineResponse422
from phrase_api.models.inline_response422_errors import InlineResponse422Errors
from phrase_api.models.invitation import Invitation
from phrase_api.models.invitation_create_parameters import InvitationCreateParameters
from phrase_api.models.invitation_update_parameters import InvitationUpdateParameters
from phrase_api.models.invitation_update_settings_parameters import InvitationUpdateSettingsParameters
from phrase_api.models.job import Job
from phrase_api.models.job_comment import JobComment
from phrase_api.models.job_comment_create_parameters import JobCommentCreateParameters
from phrase_api.models.job_comment_update_parameters import JobCommentUpdateParameters
from phrase_api.models.job_complete_parameters import JobCompleteParameters
from phrase_api.models.job_create_parameters import JobCreateParameters
from phrase_api.models.job_details import JobDetails
from phrase_api.models.job_details1 import JobDetails1
from phrase_api.models.job_keys_create_parameters import JobKeysCreateParameters
from phrase_api.models.job_locale import JobLocale
from phrase_api.models.job_locale_complete_parameters import JobLocaleCompleteParameters
from phrase_api.models.job_locale_complete_review_parameters import JobLocaleCompleteReviewParameters
from phrase_api.models.job_locale_reopen_parameters import JobLocaleReopenParameters
from phrase_api.models.job_locale_update_parameters import JobLocaleUpdateParameters
from phrase_api.models.job_locales_create_parameters import JobLocalesCreateParameters
from phrase_api.models.job_preview import JobPreview
from phrase_api.models.job_reopen_parameters import JobReopenParameters
from phrase_api.models.job_start_parameters import JobStartParameters
from phrase_api.models.job_template import JobTemplate
from phrase_api.models.job_template_create_parameters import JobTemplateCreateParameters
from phrase_api.models.job_template_details import JobTemplateDetails
from phrase_api.models.job_template_details1 import JobTemplateDetails1
from phrase_api.models.job_template_locale_update_parameters import JobTemplateLocaleUpdateParameters
from phrase_api.models.job_template_locales import JobTemplateLocales
from phrase_api.models.job_template_locales_create_parameters import JobTemplateLocalesCreateParameters
from phrase_api.models.job_template_preview import JobTemplatePreview
from phrase_api.models.job_template_update_parameters import JobTemplateUpdateParameters
from phrase_api.models.job_update_parameters import JobUpdateParameters
from phrase_api.models.key_create_parameters import KeyCreateParameters
from phrase_api.models.key_preview import KeyPreview
from phrase_api.models.key_update_parameters import KeyUpdateParameters
from phrase_api.models.keys_exclude_parameters import KeysExcludeParameters
from phrase_api.models.keys_include_parameters import KeysIncludeParameters
from phrase_api.models.keys_search_parameters import KeysSearchParameters
from phrase_api.models.keys_tag_parameters import KeysTagParameters
from phrase_api.models.keys_untag_parameters import KeysUntagParameters
from phrase_api.models.locale import Locale
from phrase_api.models.locale_create_parameters import LocaleCreateParameters
from phrase_api.models.locale_details import LocaleDetails
from phrase_api.models.locale_details1 import LocaleDetails1
from phrase_api.models.locale_preview import LocalePreview
from phrase_api.models.locale_preview1 import LocalePreview1
from phrase_api.models.locale_statistics import LocaleStatistics
from phrase_api.models.locale_team_preview import LocaleTeamPreview
from phrase_api.models.locale_update_parameters import LocaleUpdateParameters
from phrase_api.models.locale_user_preview import LocaleUserPreview
from phrase_api.models.member import Member
from phrase_api.models.member_project_detail import MemberProjectDetail
from phrase_api.models.member_project_detail_project_roles import MemberProjectDetailProjectRoles
from phrase_api.models.member_spaces import MemberSpaces
from phrase_api.models.member_update_parameters import MemberUpdateParameters
from phrase_api.models.member_update_settings_parameters import MemberUpdateSettingsParameters
from phrase_api.models.notification import Notification
from phrase_api.models.notification_group import NotificationGroup
from phrase_api.models.notification_group_detail import NotificationGroupDetail
from phrase_api.models.order_confirm_parameters import OrderConfirmParameters
from phrase_api.models.order_create_parameters import OrderCreateParameters
from phrase_api.models.project import Project
from phrase_api.models.project_create_parameters import ProjectCreateParameters
from phrase_api.models.project_details import ProjectDetails
from phrase_api.models.project_details1 import ProjectDetails1
from phrase_api.models.project_locales import ProjectLocales
from phrase_api.models.project_locales1 import ProjectLocales1
from phrase_api.models.project_member_specific import ProjectMemberSpecific
from phrase_api.models.project_short import ProjectShort
from phrase_api.models.project_update_parameters import ProjectUpdateParameters
from phrase_api.models.release import Release
from phrase_api.models.release_create_parameters import ReleaseCreateParameters
from phrase_api.models.release_preview import ReleasePreview
from phrase_api.models.release_update_parameters import ReleaseUpdateParameters
from phrase_api.models.screenshot import Screenshot
from phrase_api.models.screenshot_create_parameters import ScreenshotCreateParameters
from phrase_api.models.screenshot_marker import ScreenshotMarker
from phrase_api.models.screenshot_marker_create_parameters import ScreenshotMarkerCreateParameters
from phrase_api.models.screenshot_marker_update_parameters import ScreenshotMarkerUpdateParameters
from phrase_api.models.screenshot_update_parameters import ScreenshotUpdateParameters
from phrase_api.models.search_in_account_parameters import SearchInAccountParameters
from phrase_api.models.space import Space
from phrase_api.models.space1 import Space1
from phrase_api.models.space_create_parameters import SpaceCreateParameters
from phrase_api.models.space_update_parameters import SpaceUpdateParameters
from phrase_api.models.spaces_projects_create_parameters import SpacesProjectsCreateParameters
from phrase_api.models.styleguide import Styleguide
from phrase_api.models.styleguide_create_parameters import StyleguideCreateParameters
from phrase_api.models.styleguide_details import StyleguideDetails
from phrase_api.models.styleguide_details1 import StyleguideDetails1
from phrase_api.models.styleguide_preview import StyleguidePreview
from phrase_api.models.styleguide_update_parameters import StyleguideUpdateParameters
from phrase_api.models.subscription import Subscription
from phrase_api.models.tag import Tag
from phrase_api.models.tag_create_parameters import TagCreateParameters
from phrase_api.models.tag_with_stats import TagWithStats
from phrase_api.models.tag_with_stats1 import TagWithStats1
from phrase_api.models.tag_with_stats1_statistics import TagWithStats1Statistics
from phrase_api.models.tag_with_stats1_statistics1 import TagWithStats1Statistics1
from phrase_api.models.team import Team
from phrase_api.models.team_create_parameters import TeamCreateParameters
from phrase_api.models.team_detail import TeamDetail
from phrase_api.models.team_short import TeamShort
from phrase_api.models.team_update_parameters import TeamUpdateParameters
from phrase_api.models.teams_projects_create_parameters import TeamsProjectsCreateParameters
from phrase_api.models.teams_spaces_create_parameters import TeamsSpacesCreateParameters
from phrase_api.models.teams_users_create_parameters import TeamsUsersCreateParameters
from phrase_api.models.translation import Translation
from phrase_api.models.translation_create_parameters import TranslationCreateParameters
from phrase_api.models.translation_details import TranslationDetails
from phrase_api.models.translation_details1 import TranslationDetails1
from phrase_api.models.translation_exclude_parameters import TranslationExcludeParameters
from phrase_api.models.translation_include_parameters import TranslationIncludeParameters
from phrase_api.models.translation_key import TranslationKey
from phrase_api.models.translation_key_details import TranslationKeyDetails
from phrase_api.models.translation_key_details1 import TranslationKeyDetails1
from phrase_api.models.translation_order import TranslationOrder
from phrase_api.models.translation_review_parameters import TranslationReviewParameters
from phrase_api.models.translation_unverify_parameters import TranslationUnverifyParameters
from phrase_api.models.translation_update_parameters import TranslationUpdateParameters
from phrase_api.models.translation_verify_parameters import TranslationVerifyParameters
from phrase_api.models.translation_version import TranslationVersion
from phrase_api.models.translation_version_with_user import TranslationVersionWithUser
from phrase_api.models.translation_version_with_user1 import TranslationVersionWithUser1
from phrase_api.models.translations_exclude_parameters import TranslationsExcludeParameters
from phrase_api.models.translations_include_parameters import TranslationsIncludeParameters
from phrase_api.models.translations_review_parameters import TranslationsReviewParameters
from phrase_api.models.translations_search_parameters import TranslationsSearchParameters
from phrase_api.models.translations_unverify_parameters import TranslationsUnverifyParameters
from phrase_api.models.translations_verify_parameters import TranslationsVerifyParameters
from phrase_api.models.upload import Upload
from phrase_api.models.upload_create_parameters import UploadCreateParameters
from phrase_api.models.upload_summary import UploadSummary
from phrase_api.models.user import User
from phrase_api.models.user_preview import UserPreview
from phrase_api.models.variable import Variable
from phrase_api.models.variable_create_parameters import VariableCreateParameters
from phrase_api.models.variable_update_parameters import VariableUpdateParameters
from phrase_api.models.webhook import Webhook
from phrase_api.models.webhook_create_parameters import WebhookCreateParameters
from phrase_api.models.webhook_delivery import WebhookDelivery
from phrase_api.models.webhook_update_parameters import WebhookUpdateParameters
