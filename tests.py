import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

#Meus testes, commit 2

# 1 Testa se remover a escolha por ID remove o item correto, sobrando somente o segundo
def test_remove_choice_by_id():
    question = Question(title='q1', max_selections = 1)
    question.add_choice('a', False)
    question.add_choice('b', False)
    question.remove_choice_by_id(question.choices[0].id)
    assert len(question.choices) == 1
    assert question.choices[0].text == 'b'


# 2 Testa se remover um id invalido retorna a exceção "Invalid choice id"
def test_remove_choice_by_invalid_id_raises_exception():
    question = Question(title='q1', max_selections = 1)
    question.add_choice('a', False)
    assert len(question.choices) == 1
    with pytest.raises(Exception):
        question.remove_choice_by_id(3)

# 3 Verificar se o Remove_all_choices funciona de forma com que a lista fique vazia
def test_remove_all_choices():
    #Bem similar à anterior
    #A definição de questions poderia mesmo ser uma fixture
    question = Question(title='q1', max_selections = 1)
    question.add_choice('a', False)
    question.add_choice('b', False)
    question.remove_all_choices()
    assert len(question.choices) == 0

# 4 Testa se a exceção é lançada ao selecionar uma quantidade de escolhas maior que o limite
def test_select_choices_over_maximum_limit_raises_exception():
    question = Question(title='q1', max_selections = 1)
    question.add_choice('a', False)
    question.add_choice('b', False)
    with pytest.raises(Exception):
        question.select_choices([question.choices[0].id,question.choices[1].id])

# 5 Testa se o select_choices retorna os ids selecionados
def test_select_choices_returns_only_correct_ids():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a', False)
    question.add_choice('b', True)
    question.add_choice('c', True)
    selection = question.select_choices([question.choices[0].id,question.choices[1].id])
    assert selection == [question.choices[1].id]

# 6 Testa se select_choices retorna vazio caso não haja ids corretos
def test_select_choices_returns_empty_list_when_theres_no_correct_ids():
    question = Question(title='q1', max_selections=3)
    question.add_choice('a', False)
    question.add_choice('b', False)
    question.add_choice('c', False)
    selection = question.select_choices([question.choices[0].id,question.choices[1].id,question.choices[2].id])
    assert selection == []

# 7 Verifica se as escolhas corretas estão sendo marcadas corretamente
def test_set_correct_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    assert question.choices[0].is_correct is False
    question.set_correct_choices([question.choices[0].id])
    assert question.choices[0].is_correct is True

# 8 Testa a configuração sequencial dos IDs das escolhas
def test_set_sequential_choice_ids():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a', False)
    question.add_choice('b', False)
    question.add_choice('c', False)
    assert question.choices[1].id == question.choices[0].id + 1
    assert question.choices[2].id == question.choices[1].id + 1

# 9 Testa a configuração sequencial dos IDs das escolhas, no caso em que foram removidas escolhas e o ID não acompanha o índice
def test_set_sequential_choice_ids_different_from_index():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a', False) #criado com id 1
    question.add_choice('b', False) #criado com id 2
    question.add_choice('c', False) #criado com id 3
    question.add_choice('d', False) #criado com id 4
    question.add_choice('e', False) #criado com id 5
    question.remove_choice_by_id(3)
    assert question.choices[1].id == question.choices[0].id + 1
    assert question.choices[2].id == question.choices[1].id + 2

# 10 Testa se ao criar uma nova pergunta os IDs são criados do zero
def test_set_new_sequential_choice_ids_for_new_question():
    question1 = Question(title='q1', max_selections=2)
    question1.add_choice('a', False)
    question1.add_choice('b', False)
    question1.add_choice('c', False)
    question2 = Question(title='q1', max_selections=2)
    question2.add_choice('a', False)
    question2.add_choice('b', False)
    question2.add_choice('c', False)
    assert question1.choices[0].id == 1
    assert question2.choices[0].id == 1