from server.models.postgis.mapping_issues import MappingIssueCategory
from server.models.postgis.task import TaskMappingIssue
from server.models.dtos.mapping_issues_dto import MappingIssueCategoryDTO

class MappingIssueCategoryService:

    @staticmethod
    def get_mapping_issue_category(category_id: int) -> MappingIssueCategory:
        """
        Get MappingIssueCategory from DB
        :raises: NotFound
        """
        category = MappingIssueCategory.get_by_id(category_id)

        if category is None:
            raise NotFound()

        return category

    @staticmethod
    def get_mapping_issue_category_as_dto(category_id: int) -> MappingIssueCategoryDTO:
        """ Get MappingIssueCategory from DB """
        category = MappingIssueCategoryService.get_mapping_issue_category(category_id)
        return category.as_dto()

    @staticmethod
    def create_mapping_issue_category(category_dto: MappingIssueCategoryDTO) -> int:
        """ Create MappingIssueCategory in DB """
        new_mapping_issue_category_id = MappingIssueCategory.create_from_dto(category_dto)
        return new_mapping_issue_category_id

    @staticmethod
    def update_mapping_issue_category(category_dto: MappingIssueCategoryDTO) -> MappingIssueCategoryDTO:
        """ Create MappingIssueCategory in DB """
        category = MappingIssueCategoryService.get_mapping_issue_category(category_dto.category_id)
        category.update_category(category_dto)
        return category.as_dto()

    @staticmethod
    def delete_mapping_issue_category(category_id: int):
        """ Delete specified license"""
        category = MappingIssueCategoryService.get_mapping_issue_category(category_id)
        category.delete()

    @staticmethod
    def get_all_mapping_issue_categories(include_archived):
        """ Get all mapping issue categories"""
        return MappingIssueCategory.get_all_categories(include_archived)


class MappingIssueService:

    @staticmethod
    def get_all_mapping_issues():
        """
        Get all issues from db
        raises: NotFound
        """
        
        mappingIssueList = TaskMappingIssue.get_all_issues()

        if mappingIssueList is None:
            raise NotFound()
        else:
            #Sum the counts of all entries of the same category and convert to csv
            issueCount = TaskMappingIssue.get_issue_row_count()
            issues = []
            summedIssue = TaskMappingIssue("Issue", "Count", "CategoryID") #csv table column names

            i = 0
            for issue in mappingIssueList:
                if ((issue.mapping_issue_category_id != summedIssue.mapping_issue_category_id) or (i == 0)): 
                    issues.append(summedIssue)
                    summedIssue = issue
                else:
                    summedIssue.count += issue.count
                if (i == (issueCount - 1)):
                    issues.append(summedIssue)
                i += 1

            csvIssues = []
            for issue in issues:
                issueProperties = [str(issue.mapping_issue_category_id), 
                                   str(issue.issue),
                                   str(issue.count)]
                csvIssue = ",".join(issueProperties)
                csvIssues.append(csvIssue)
                
            csvString = "\n".join(csvIssues)
            return csvString
