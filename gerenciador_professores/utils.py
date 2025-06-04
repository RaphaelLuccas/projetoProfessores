from datetime import datetime

def validar_e_formatar_cpf(P):
    cpf_limpo = ''.join(filter(str.isdigit, P))

    if len(cpf_limpo) > 11:
        cpf_limpo = cpf_limpo[:11]

    if len(cpf_limpo) > 9:
        return f"{cpf_limpo[0:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    elif len(cpf_limpo) > 6:
        return f"{cpf_limpo[0:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:]}"
    elif len(cpf_limpo) > 3:
        return f"{cpf_limpo[0:3]}.{cpf_limpo[3:]}"
    else:
        return cpf_limpo


def formatar_cpf_display(cpf_raw):
    cpf_limpo = ''.join(filter(str.isdigit, cpf_raw))
    if len(cpf_limpo) == 11:
        return f"{cpf_limpo[0:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    return cpf_raw

def formatar_data(data_str):
    return datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')
