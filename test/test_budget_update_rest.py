from code import budget_update
from mock import ANY
from mock import Mock
from mock.mock import patch
from telebot import types


@patch('telebot.telebot')
def test_update_overall_budget_already_available_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(budget_update, 'helper')
    budget_update.helper.getCurrencies.return_value = ['USD', 'EUR', 'INR']

    message = Mock()
    message.text = 'USD'
    budget_update.update_overall_budget(message, mc)
    mc.reply_to.assert_called_with(message, 'Select Currency', reply_markup=ANY)


@patch('telebot.telebot')
def test_update_overall_budget_new_budget_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(budget_update, 'helper')
    budget_update.helper.getCurrencies.return_value = ['USD', 'EUR', 'INR']
    budget_update.helper.isOverallBudgetAvailable.return_value = True

    message = Mock()
    message.text = 'USD'
    budget_update.update_overall_budget(message, mc)
    mc.reply_to.assert_called_with(message, 'Select Currency', reply_markup=ANY)


@patch('telebot.telebot')
def test_post_overall_amount_input_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(budget_update, 'helper')
    budget_update.helper.isOverallBudgetAvailable.return_value = True
    budget_update.helper.validate_entered_amount.return_value = 150

    message = create_message("hello from testing")
    budget_update.post_overall_amount_input(message, mc, 'INR')

    mc.send_message.assert_called_with(11, ANY)


@patch('telebot.telebot')
def test_post_overall_amount_input_nonworking(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(budget_update, 'helper')
    budget_update.helper.getCurrencies.return_value = ['USD', 'EUR', 'INR']
    budget_update.helper.isOverallBudgetAvailable.return_value = True

    message = Mock()
    message.text = 'USD'
    budget_update.update_overall_budget(message, mc)
    mc.reply_to.assert_called_with(message, 'Select Currency', reply_markup=ANY)


@patch('telebot.telebot')
def test_update_category_budget(mock_telebot, mocker):
    mc = mock_telebot.return_value
    reply_message = create_message("Food")
    mc.reply_to.return_value = reply_message

    mocker.patch.object(budget_update, 'helper')
    budget_update.helper.getSpendCategories.return_value = ['Food', 'Groceries', 'Utilities', 'Transport', 'Shopping', 'Miscellaneous']

    message = create_message("hello from testing")
    budget_update.update_category_budget(message, mc)

    mc.reply_to.assert_called_with(message, 'Select Category', reply_markup=ANY)


@patch('telebot.telebot')
def test_post_category_selection_category_not_found(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(budget_update, 'helper')
    budget_update.helper.getSpendCategories.return_value = []
    budget_update.helper.throw_exception.return_value = True

    message = create_message("hello from testing")
    budget_update.post_category_selection(message, mc)

    mc.send_message.assert_called_with(11, 'Invalid', reply_markup=ANY)
    assert (budget_update.helper.throw_exception.called)


@patch('telebot.telebot')
def test_post_category_selection_category_wise_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    reply_message = create_message("Food")
    mc.reply_to.return_value = reply_message

    mocker.patch.object(budget_update, 'helper')
    budget_update.helper.getSpendCategories.return_value = ['Food', 'Groceries', 'Utilities', 'Transport', 'Shopping', 'Miscellaneous']
    budget_update.helper.getCurrencies.return_value = ['USD', 'EUR', 'GBP', 'INR', 'JPY']

    message = create_message("Food")
    budget_update.post_category_selection(message, mc)

    mc.reply_to.assert_called_with(message, 'Select Currency', reply_markup=ANY)


@patch('telebot.telebot')
def test_post_category_selection_overall_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    reply_message = create_message("Food")
    mc.reply_to.return_value = reply_message

    mocker.patch.object(budget_update, 'helper')
    budget_update.helper.getSpendCategories.return_value = ['Food', 'Groceries', 'Utilities', 'Transport', 'Shopping', 'Miscellaneous']
    budget_update.helper.getCurrencies.return_value = ['USD', 'EUR', 'GBP', 'INR', 'JPY']

    message = create_message("Food")
    budget_update.post_category_selection(message, mc)


    mc.reply_to.assert_called_with(message, 'Select Currency', reply_markup=ANY)


@patch('telebot.telebot')
def test_post_category_amount_input_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(budget_update, 'helper')
    budget_update.helper.validate_entered_amount.return_value = 100

    message = create_message("Hello from testing")
    budget_update.post_category_amount_input(message, mc, "Food", 'INR')

    mc.send_message.assert_called_with(11, 'Budget for Food Created!')


@patch('telebot.telebot')
def test_post_category_amount_input_nonworking_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    reply_message = create_message("100")
    mc.send_message.return_value = reply_message

    mocker.patch.object(budget_update, 'helper')
    mocker.patch.object(budget_update, 'currencies')
    budget_update.helper.validate_entered_amount.return_value = 100
    budget_update.currencies.convert.return_value = 73.5
    budget_update.helper.read_json.return_value = {}
    budget_update.helper.createNewUserRecord.return_value = {'budget': {'category': None}}
    budget_update.helper.write_json.return_value = True

    message = create_message("Food")
    budget_update.post_category_amount_input(message, mc, "Food", "INR")

    mc.send_message.assert_called_with(11, 'Budget for Food Created!')
    assert (budget_update.helper.write_json.called)


@patch('telebot.telebot')
def test_post_category_add(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True

    message = create_message("hello from testing!")
    budget_update.post_category_add(message, mc)

    mc.reply_to.assert_called_with(message, 'Select Option', reply_markup=ANY)


def create_message(text):
    params = {'messagebody': text}
    chat = types.User(11, False, 'test')
    message = types.Message(1, None, None, chat, 'text', params, "")
    message.text = text
    return message
