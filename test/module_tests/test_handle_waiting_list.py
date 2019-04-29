from test.unit_tests.minicrmtestbase import MiniCrmTestBase
from functionalities.handlewaitinglist import handle_waiting_list
import test.minicrm_api_mock.api_outputs as apioutputs
import test.minicrm_api_mock.apioutputs.general as apioutputs_general
import test.minicrm_api_mock.apioutputs.students as apioutputs_students


class TestHandleWaitingList(MiniCrmTestBase):

    def test_there_is_one_student_on_waiting_list_but_there_are_no_free_places_do_nothing(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2750),
            apioutputs.API_OUTPUTS['waiting_list_one_student_status_2750'])
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2790),
            apioutputs_students.FAKE_STUDENT)
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs.API_OUTPUTS['course_list_for_course_code']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            apioutputs.API_OUTPUTS['project_2037_2019-1_Q_full']
        )
        self.set_participant_number_expectations()
        handle_waiting_list(self.crm_data)

    def test_there_are_multiple_students_on_waiting_list_but_there_are_no_free_places_do_nothing(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2750),
            apioutputs.API_OUTPUTS['waiting_list_two_students_status_2750'])
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2790),
            apioutputs_students.FAKE_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2796),
            apioutputs_students.FAKE_STUDENT_APPLIED_LATER)
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs.API_OUTPUTS['course_list_for_course_code']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            apioutputs.API_OUTPUTS['project_2037_2019-1_Q_full']
        )
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs.API_OUTPUTS['course_list_for_course_code']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            apioutputs.API_OUTPUTS['project_2037_2019-1_Q_full']
        )
        self.set_participant_number_expectations()
        handle_waiting_list(self.crm_data)

    def test_there_is_one_student_on_waiting_list_and_there_is_one_free_place_put_student_to_info_sent(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2750),
            apioutputs.API_OUTPUTS['waiting_list_one_student_status_2750'])
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2790),
            apioutputs_students.FAKE_STUDENT)
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs.API_OUTPUTS['course_list_for_course_code']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            apioutputs.API_OUTPUTS['project_2037_2019-1_Q_one_place_free'])
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(
                2601,
                {
                    u"StatusId":u"2781",
                    u"Levelkuldesek":u"Kezd\u0151 INFO lev\u00e9l, Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"
                }
            ),
            apioutputs_general.XPUT_RESPONSE
        )
        self.set_participant_number_expectations()
        handle_waiting_list(self.crm_data)

    def test_there_are_multiple_students_on_waiting_list_and_there_is_one_free_place_put_earlier_student_to_info_sent(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2750),
            apioutputs.API_OUTPUTS['waiting_list_two_students_status_2750'])
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2790),
            apioutputs_students.FAKE_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2796),
            apioutputs_students.FAKE_STUDENT_APPLIED_LATER)
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs.API_OUTPUTS['course_list_for_course_code']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            apioutputs.API_OUTPUTS['project_2037_2019-1_Q_one_place_free'])
        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(
                2601,
                {
                    u"StatusId":u"2781",
                    u"Levelkuldesek":u"Kezd\u0151 INFO lev\u00e9l, Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"
                }
            ),
            apioutputs_general.XPUT_RESPONSE
        )
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs.API_OUTPUTS['course_list_for_course_code']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            apioutputs.API_OUTPUTS['project_2037_2019-1_Q_full']
        )
        self.set_participant_number_expectations()
        handle_waiting_list(self.crm_data)

    def test_there_are_multiple_students_on_waiting_list_and_there_are_two_free_places_put_both_students_to_info_sent(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2750),
            apioutputs.API_OUTPUTS['waiting_list_two_students_status_2750'])
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2790),
            apioutputs_students.FAKE_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2796),
            apioutputs_students.FAKE_STUDENT_APPLIED_LATER)
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs.API_OUTPUTS['course_list_for_course_code']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            apioutputs.API_OUTPUTS['project_2037_2019-1_Q_one_place_free'])

        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(
                2601,
                {
                    u"StatusId": u"2781",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"
                }
            ),
            apioutputs_general.XPUT_RESPONSE
        )
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs.API_OUTPUTS['course_list_for_course_code']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            apioutputs.API_OUTPUTS['project_2037_2019-1_Q_one_place_free']
        )

        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(
                2602,
                {
                    u"StatusId": u"2781",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"
                }
            ),
            apioutputs_general.XPUT_RESPONSE
        )
        self.set_participant_number_expectations()
        handle_waiting_list(self.crm_data)

    def test_there_are_5_students_on_the_waiting_list_and_there_are_two_free_places_put_the_earliest_two_to_info_sent(self):
        self.command_handler.expect_command(
            self.crm_command_factory.get_project_list_for_status(2750),
            apioutputs.API_OUTPUTS['waiting_list_five_students_status_2750'])
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2798),
            apioutputs_students.FAKE_STUDENT)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2790),
            apioutputs_students.FAKE_STUDENT_APPLIED_LATER)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2799),
            apioutputs_students.FAKE_STUDENT_APPLIED_LATER)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2796),
            apioutputs_students.FAKE_STUDENT_4TH_APPLIED)
        self.command_handler.expect_command(
            self.crm_command_factory.get_student(2797),
            apioutputs_students.FAKE_STUDENT_5TH_APPLIED)

        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs.API_OUTPUTS['course_list_for_course_code']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            apioutputs.API_OUTPUTS['project_2037_2019-1_Q_one_place_free'])

        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(
                2601,
                {
                    u"StatusId": u"2781",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"
                }
            ),
            apioutputs_general.XPUT_RESPONSE
        )
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs.API_OUTPUTS['course_list_for_course_code']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            apioutputs.API_OUTPUTS['project_2037_2019-1_Q_one_place_free']
        )

        self.command_handler.expect_command(
            self.crm_command_factory.set_project_data(
                2602,
                {
                    u"StatusId": u"2781",
                    u"Levelkuldesek": u"Kezd\u0151 INFO lev\u00e9l, Kezd\u0151 INFO lev\u00e9l, Felszabadult egy hely"
                }
            ),
            apioutputs_general.XPUT_RESPONSE
        )

        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs.API_OUTPUTS['course_list_for_course_code']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            apioutputs.API_OUTPUTS['project_2037_2019-1_Q_full']
        )
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs.API_OUTPUTS['course_list_for_course_code']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            apioutputs.API_OUTPUTS['project_2037_2019-1_Q_full']
        )
        self.set_participant_number_expectations()
        self.command_handler.expect_command(
            self.crm_command_factory.get_course_list_by_course_code("2019-1-Q"),
            apioutputs.API_OUTPUTS['course_list_for_course_code']
        )
        self.command_handler.expect_command(
            self.crm_command_factory.get_course(1164),
            apioutputs.API_OUTPUTS['project_2037_2019-1_Q_full']
        )

        self.set_participant_number_expectations()
        handle_waiting_list(self.crm_data)